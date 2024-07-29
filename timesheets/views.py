from django.shortcuts import render, redirect, get_object_or_404
from .models import Timesheet, calculate_total_charge
from .forms import TimesheetForm
from django.contrib.auth.decorators import login_required
from customers.models import Customer
from django.http import HttpResponse
from decimal import Decimal, ROUND_UP
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from django.contrib import messages

@login_required
def timesheet_create(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    confirm_no_file = False
    if request.method == 'POST':
        form = TimesheetForm(request.POST, request.FILES)
        if form.is_valid():
            timesheet = form.save(commit=False)
            timesheet.customer = customer

            # Check for duplicate Timesheet ID and append suffix if needed
            base_id = timesheet.timesheet_id
            suffix = 1
            while Timesheet.objects.filter(timesheet_id=timesheet.timesheet_id).exists():
                timesheet.timesheet_id = f"{base_id}-{suffix}"
                suffix += 1

            # Check if no file uploaded
            if not timesheet.file and 'confirm_no_file' not in request.POST:
                confirm_no_file = True
            else:
                # Handle pause logic and calculate total charge
                rate_dict = {
                    1: (customer.tech1_regular_hours, customer.tech1_time_and_a_half_hours, customer.tech1_double_time_hours),
                    2: (customer.tech2_regular_hours, customer.tech2_time_and_a_half_hours, customer.tech2_double_time_hours),
                    3: (customer.tech3_regular_hours, customer.tech3_time_and_a_half_hours, customer.tech3_double_time_hours),
                }
                regular_rate, time_and_a_half_rate, double_time_rate = rate_dict[timesheet.technician_level]

                # Convert time_in and time_out to datetime objects for the same date
                datetime_in = make_aware(datetime.combine(datetime.strptime(timesheet.date, '%Y/%m/%d').date(), datetime.strptime(timesheet.time_in, '%H:%M').time()))
                datetime_out = make_aware(datetime.combine(datetime.strptime(timesheet.date, '%Y/%m/%d').date(), datetime.strptime(timesheet.time_out, '%H:%M').time()))

                # Calculate pause duration in hours
                pause_duration = Decimal(0)
                if timesheet.pause_hours is not None and timesheet.pause_minutes is not None:
                    pause_duration = Decimal(timesheet.pause_hours + timesheet.pause_minutes / 60)

                if timesheet.special_rate:
                    # Calculate the total time used in hours
                    total_time_used = Decimal((datetime_out - datetime_in).total_seconds() / 3600) - pause_duration
                    # Round the total time used up to the nearest 15 minutes
                    rounded_minutes = (total_time_used * 60 + 14) // 15 * 15
                    rounded_hours = Decimal(rounded_minutes) / 60
                    total_charge = timesheet.special_rate * rounded_hours
                else:
                    total_charge, total_time_used = calculate_total_charge(timesheet, regular_rate, time_and_a_half_rate, double_time_rate)
                    total_charge -= regular_rate * pause_duration  # Subtract pause duration charge

                # Handle manual charges
                if timesheet.manual_charge_hours is not None and timesheet.manual_charge_amount is not None:
                    total_charge = timesheet.manual_charge_amount
                    total_time_used = timesheet.manual_charge_hours

                timesheet.total_charge = total_charge
                timesheet.total_time_used = total_time_used
                timesheet.save()
                return redirect('timesheets:list', customer_id=customer.id)
    else:
        form = TimesheetForm()
    return render(request, 'timesheets/timesheet_create.html', {'form': form, 'customer': customer, 'confirm_no_file': confirm_no_file})

@login_required
def timesheet_edit(request, pk):
    timesheet = get_object_or_404(Timesheet, pk=pk)
    if request.method == 'POST':
        form = TimesheetForm(request.POST, request.FILES, instance=timesheet)
        if form.is_valid():
            form.save()
            return redirect('timesheets:list', customer_id=timesheet.customer.id)
    else:
        form = TimesheetForm(instance=timesheet)
    return render(request, 'timesheets/timesheet_edit.html', {'form': form, 'timesheet': timesheet})

@login_required
def timesheets_list(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    timesheets = Timesheet.objects.filter(customer=customer)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y/%m/%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y/%m/%d')
        timesheets = timesheets.filter(date__range=[start_date, end_date])

    total_charge = sum(timesheet.total_charge for timesheet in timesheets)
    total_time_used = sum(timesheet.total_time_used for timesheet in timesheets if timesheet.total_time_used)

    return render(request, 'timesheets/timesheets_list.html', {
        'timesheets': timesheets,
        'customer': customer,
        'total_charge': total_charge,
        'total_time_used': total_time_used,
        'start_date': start_date,
        'end_date': end_date,
    })

@login_required
def timesheet_delete(request, pk):
    timesheet = get_object_or_404(Timesheet, pk=pk)
    customer_id = timesheet.customer.id  # Get the customer ID before deleting the timesheet
    if request.method == 'POST':
        timesheet.delete()
        return redirect('timesheets:list', customer_id=customer_id)  # Ensure redirection includes the customer ID
    return render(request, 'timesheets/timesheet_confirm_delete.html', {'timesheet': timesheet, 'customer_id': customer_id})

def upload_test(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['testfile']
        with open('some_path_to_save_file', 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        return HttpResponse("File uploaded successfully")
    return render(request, 'timesheets/upload_test.html')

@login_required
def approve_timesheet(request, pk):
    timesheet = get_object_or_404(Timesheet, pk=pk)
    if request.method == 'POST':
        timesheet.approved = True
        timesheet.save()
        messages.success(request, 'Timesheet approved successfully.')
    return redirect('timesheets:list', customer_id=timesheet.customer.id)

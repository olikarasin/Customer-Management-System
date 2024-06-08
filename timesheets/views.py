# timesheets/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Timesheet, calculate_total_charge
from .forms import TimesheetForm
from django.contrib.auth.decorators import login_required
from customers.models import Customer
from django.http import HttpResponse
from decimal import Decimal
from django.utils.timezone import make_aware
from datetime import datetime, timedelta

@login_required
def timesheet_create(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        form = TimesheetForm(request.POST, request.FILES)
        if form.is_valid():
            timesheet = form.save(commit=False)
            timesheet.customer = customer
            
            # Define the technician rates based on the level
            rate_dict = {
                1: (customer.tech1_regular_hours, customer.tech1_time_and_a_half_hours, customer.tech1_double_time_hours),
                2: (customer.tech2_regular_hours, customer.tech2_time_and_a_half_hours, customer.tech2_double_time_hours),
                3: (customer.tech3_regular_hours, customer.tech3_time_and_a_half_hours, customer.tech3_double_time_hours),
            }
            regular_rate, time_and_a_half_rate, double_time_rate = rate_dict[timesheet.technician_level]

            # Calculate the total charge
            if timesheet.special_rate:
                total_charge, total_time_used = timesheet.special_rate, (timesheet.time_out - timesheet.time_in).total_seconds() / 3600
            else:
                total_charge, total_time_used = calculate_total_charge(timesheet, regular_rate, time_and_a_half_rate, double_time_rate)
            
            timesheet.total_charge = total_charge
            timesheet.total_time_used = total_time_used
            customer.hours_remaining -= total_time_used
            customer.save()
            timesheet.save()
            return redirect('timesheets:list', customer_id=customer.id)
    else:
        form = TimesheetForm()
    return render(request, 'timesheets/timesheet_create.html', {'form': form, 'customer': customer})

@login_required
def timesheets_list(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    timesheets = Timesheet.objects.filter(customer=customer)
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
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
        timesheet.customer.hours_remaining += timesheet.total_time_used
        timesheet.customer.save()
        timesheet.delete()
        return redirect('timesheets:list', customer_id=customer_id)  # Ensure redirection includes the customer ID
    return render(request, 'timesheets/timesheet_confirm_delete.html', {'timesheet': timesheet, 'customer_id': customer_id})

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

def upload_test(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['testfile']
        with open('some_path_to_save_file', 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        return HttpResponse("File uploaded successfully")
    return render(request, 'timesheets/upload_test.html')

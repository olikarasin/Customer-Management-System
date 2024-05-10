from django.shortcuts import render, redirect, get_object_or_404
from .models import Timesheet
from .forms import TimesheetForm
from django.contrib.auth.decorators import login_required
from customers.models import Customer
# For testing
from django.http import HttpResponse


@login_required
def timesheet_create(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        form = TimesheetForm(request.POST, request.FILES)
        if form.is_valid():
            timesheet = form.save(commit=False)
            timesheet.customer = customer
            # Make sure rate is set before saving, example default handling:
            if not timesheet.rate:
                timesheet.rate = Decimal("0.00")  # Default rate if not provided
            timesheet.save()
            return redirect('timesheets:list', customer_id=customer.id)
    else:
        form = TimesheetForm()
    return render(request, 'timesheets/timesheet_create.html', {'form': form, 'customer': customer})

@login_required
def timesheets_list(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    timesheets = Timesheet.objects.filter(customer=customer)
    return render(request, 'timesheets/timesheets_list.html', {'timesheets': timesheets, 'customer': customer})

@login_required
def timesheet_edit(request, pk):
    timesheet = get_object_or_404(Timesheet, pk=pk)
    if request.method == 'POST':
        form = TimesheetForm(request.POST, request.FILES, instance=timesheet)
        if form.is_valid():
            form.save()
            return redirect('timesheets:list', customer_id=timesheet.customer.id)  # Ensure redirection includes the customer ID
    else:
        form = TimesheetForm(instance=timesheet)
    return render(request, 'timesheets/timesheet_edit.html', {'form': form, 'timesheet': timesheet})

@login_required
def timesheet_delete(request, pk):
    timesheet = get_object_or_404(Timesheet, pk=pk)
    if request.method == 'POST':
        timesheet.delete()
        return redirect('timesheets:list', customer_id=timesheet.customer.id)  # Adjust the redirect to include the customer ID
    return render(request, 'timesheets/timesheet_confirm_delete.html', {'timesheet': timesheet})

# Test file
def upload_test(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['testfile']
        with open('some_path_to_save_file', 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        return HttpResponse("File uploaded successfully")
    return render(request, 'timesheets/upload_test.html')
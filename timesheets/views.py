from django.shortcuts import render, redirect, get_object_or_404
from .models import Timesheet
from .forms import TimesheetForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from customers.models import Customer

@login_required
def timesheet_create(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        form = TimesheetForm(request.POST, request.FILES)
        if form.is_valid():
            timesheet = form.save(commit=False)
            timesheet.customer = customer
            timesheet.save()
            return redirect('timesheets:list', customer_id=customer.id)  # Ensure correct redirection
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
            return redirect('timesheets:list', customer_id=timesheet.customer.id)  # Make sure the redirection is correct
    else:
        form = TimesheetForm(instance=timesheet)
    return render(request, 'timesheets/timesheet_edit.html', {'form': form, 'timesheet': timesheet})

@login_required
def timesheet_delete(request, pk):
    timesheet = get_object_or_404(Timesheet, pk=pk)
    if request.method == 'POST':
        timesheet.delete()
        return redirect('timesheets:list')  # Adjust the redirect if needed
    # You might want to add a confirmation page before deleting
    return render(request, 'timesheets/timesheet_confirm_delete.html', {'timesheet': timesheet})


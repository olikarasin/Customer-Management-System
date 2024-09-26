from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Customer, EmailReference, Technician, Contract, Credential, Timesheet
from .forms import CustomerForm, EmailReferenceForm, ContractForm, TechnicianForm, CredentialForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from accounts.models import UserProfile
import random
import string

# Helper functions to check user roles
def is_admin(user):
    return user.is_authenticated and user.is_staff

def is_customer(user):
    return user.is_authenticated and not user.is_staff

def main_login(request):
    return render(request, 'accounts/main_login.html')

@login_required
@user_passes_test(is_admin)
def customer_list(request):
    query = request.GET.get('q', '')
    if query:
        customers = Customer.objects.filter(Q(name__icontains=query))
    else:
        customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})

# @login_required
# @user_passes_test(is_admin)
# def customer_create(request):
#     if request.method == 'POST':
#         form = CustomerForm(request.POST)
#         if form.is_valid():
#             customer = form.save()
#             emails = request.POST.getlist('emails')
#             for email in emails:
#                 if email:
#                     email_ref, created = EmailReference.objects.get_or_create(email=email)
#                     customer.emails.add(email_ref)
#             return redirect('customers:list')
#     else:
#         form = CustomerForm()
#     return render(request, 'customers/customer_create.html', {'form': form})

from django.shortcuts import get_object_or_404, redirect
from .models import Customer
from .forms import CustomerForm

def customer_create(request):
    if request.method == 'POST':
        user_profile = request.user  # Assuming the user is logged in and tied to the profile
        # Use get_or_create to prevent duplicate customers
        customer, created = Customer.objects.get_or_create(user_profile=user_profile)

        if not created:
            # Customer already exists, update it
            form = CustomerForm(request.POST, instance=customer)
        else:
            # New customer
            form = CustomerForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect('some_view')  # Redirect to an appropriate view after saving

@login_required
@user_passes_test(is_admin)
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save()
            customer.emails.clear()
            emails = request.POST.getlist('emails')
            for email in emails:
                if email:
                    email_ref, created = EmailReference.objects.get_or_create(email=email)
                    customer.emails.add(email_ref)
            return redirect('customers:list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_edit.html', {'form': form, 'customer': customer})

@login_required
@user_passes_test(is_admin)
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customers:list')
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})

@login_required
@user_passes_test(is_customer)
def customer_dashboard(request):
    credentials = Credential.objects.filter(username=request.user.username)
    if credentials.exists():
        customer = credentials.first().customer
        timesheets = customer.customer_timesheets.all()
        return render(request, 'customers/customer_dashboard.html', {'customer': customer, 'timesheets': timesheets})
    else:
        messages.error(request, "No customer information found.")
        return redirect('accounts:login')

@login_required
@user_passes_test(is_admin)
def contract_list(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    contracts = Contract.objects.filter(customer=customer)
    return render(request, 'customers/contract_list.html', {'contracts': contracts, 'customer': customer})

@login_required
@user_passes_test(is_admin)
def contract_create(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.customer = customer
            contract.save()
            return redirect('customers:contract_list', customer_id=customer.id)
    else:
        form = ContractForm()
    return render(request, 'customers/contract_create.html', {'form': form, 'customer': customer})

@login_required
@user_passes_test(is_admin)
def contract_edit(request, customer_id, pk):
    contract = get_object_or_404(Contract, pk=pk, customer_id=customer_id)
    if request.method == 'POST':
        form = ContractForm(request.POST, instance=contract)
        if form.is_valid():
            form.save()
            return redirect('customers:contract_list', customer_id=customer_id)
    else:
        form = ContractForm(instance=contract)
    return render(request, 'customers/contract_edit.html', {'form': form, 'customer_id': customer_id, 'contract': contract})

@login_required
@user_passes_test(is_admin)
def contract_delete(request, customer_id, pk):
    contract = get_object_or_404(Contract, pk=pk, customer_id=customer_id)
    if request.method == 'POST':
        contract.delete()
        return redirect('customers:contract_list', customer_id=customer_id)
    return render(request, 'customers/contract_confirm_delete.html', {'contract': contract, 'customer_id': customer_id})

@login_required
@user_passes_test(is_admin)
def contract_approve(request, customer_id, pk):
    contract = get_object_or_404(Contract, pk=pk, customer_id=customer_id)
    if request.method == 'POST':
        contract.approved = True
        contract.save()
        messages.success(request, 'Contract approved successfully.')
    return redirect('customers:contract_list', customer_id=contract.customer.id)

@login_required
@user_passes_test(is_admin)
def credential_list(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    credentials = Credential.objects.filter(customer=customer)
    return render(request, 'customers/credential_list.html', {'credentials': credentials, 'customer': customer})

# @login_required
# @user_passes_test(is_admin)
# def credential_create(request, customer_id):
#     customer = get_object_or_404(Customer, pk=customer_id)
#     if request.method == 'POST':
#         form = CredentialForm(request.POST)
#         if form.is_valid():
#             credential = form.save(commit=False)
#             credential.customer = customer
#             credential.password = request.POST.get('password', 'default_password')  # No hashing
#             credential.save()
#             return redirect('customers:credential_list', customer_id=customer.id)
#     else:
#         form = CredentialForm()
#     return render(request, 'customers/credential_create.html', {'form': form, 'customer': customer})

@login_required
@user_passes_test(is_admin)
def credential_create(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    
    # Check if a Credential already exists for the Customer
    credential, created = Credential.objects.get_or_create(customer=customer)
    
    if request.method == 'POST':
        form = CredentialForm(request.POST, instance=credential)  # Pass the existing credential if it exists
        if form.is_valid():
            credential = form.save(commit=False)
            credential.customer = customer
            credential.password = request.POST.get('password', 'default_password')  # No hashing
            credential.save()
            return redirect('customers:credential_list', customer_id=customer.id)
    else:
        form = CredentialForm(instance=credential)  # Populate the form with the existing credential, if any
    
    return render(request, 'customers/credential_create.html', {'form': form, 'customer': customer})

@login_required
@user_passes_test(is_admin)
def credential_edit(request, customer_id, pk):
    credential = get_object_or_404(Credential, pk=pk, customer_id=customer_id)
    if request.method == 'POST':
        form = CredentialForm(request.POST, instance=credential)
        if form.is_valid():
            credential = form.save(commit=False)
            if 'password' in form.changed_data:
                credential.password = request.POST.get('password')  # No hashing
            credential.save()
            return redirect('customers:credential_list', customer_id=customer_id)
    else:
        form = CredentialForm(instance=credential)
    return render(request, 'customers/credential_edit.html', {'form': form, 'customer_id': customer_id, 'credential': credential})

@login_required
@user_passes_test(is_admin)
def credential_delete(request, customer_id, pk):
    credential = get_object_or_404(Credential, pk=pk, customer_id=customer_id)
    if request.method == 'POST':
        credential.delete()
        return redirect('customers:credential_list', customer_id=customer_id)
    return render(request, 'customers/credential_confirm_delete.html', {'credential': credential, 'customer_id': customer_id})

@login_required
@user_passes_test(is_admin)
def technician_list(request):
    technicians = Technician.objects.all()
    return render(request, 'customers/technician_list.html', {'technicians': technicians})

@login_required
@user_passes_test(is_admin)
def technician_create(request):
    if request.method == 'POST':
        form = TechnicianForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customers:technician_list')
    else:
        form = TechnicianForm()
    return render(request, 'customers/technician_create.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def technician_delete(request, pk):
    technician = get_object_or_404(Technician, pk=pk)
    if request.method == 'POST':
        technician.delete()
        return redirect('customers:technician_list')
    return render(request, 'customers/technician_confirm_delete.html', {'technician': technician})

def generate_password(request):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(10))
    return HttpResponse(password)

@login_required
@user_passes_test(is_admin)
def reports(request):
    customers = Customer.objects.filter(status='Active')
    return render(request, 'customers/reports.html', {'customers': customers})

@login_required
@user_passes_test(is_admin)
def update_renewal_status(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        customer.renewal_paid = not customer.renewal_paid
        customer.save()
    return redirect('customers:reports')

@login_required
@user_passes_test(is_admin)
def delete_timesheets_older_than_6_months(request):
    six_months_ago = timezone.now() - timedelta(days=182)
    timesheets_to_delete = Timesheet.objects.filter(date__lt=six_months_ago)
    timesheets_deleted, _ = timesheets_to_delete.delete()
    messages.success(request, f"Deleted {timesheets_deleted} timesheets older than 6 months.")
    return redirect('customers:squash')

@login_required
@user_passes_test(is_admin)
def delete_timesheets_of_inactive_customers(request):
    timesheets_to_delete = Timesheet.objects.filter(customer__status='Inactive')
    timesheets_deleted, _ = timesheets_to_delete.delete()
    messages.success(request, f"Deleted {timesheets_deleted} timesheets of inactive customers.")
    return redirect('customers:squash')

@login_required
@user_passes_test(is_admin)
def delete_timesheets_in_range(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            timesheets_to_delete = Timesheet.objects.filter(date__range=[start_date, end_date])
            timesheets_deleted, _ = timesheets_to_delete.delete()
            messages.success(request, f"Deleted {timesheets_deleted} timesheets in the specified range.")
        else:
            messages.error(request, "Please provide both start and end dates.")
    return redirect('customers:squash')

@login_required
@user_passes_test(is_admin)
def delete_timesheets_older_than_date(request):
    if request.method == 'POST':
        specific_date = request.POST.get('specific_date')
        if specific_date:
            timesheets_to_delete = Timesheet.objects.filter(date__lt=specific_date)
            timesheets_deleted, _ = timesheets_to_delete.delete()
            messages.success(request, f"Deleted {timesheets_deleted} timesheets older than the specified date.")
        else:
            messages.error(request, "Please provide a specific date.")
    return redirect('customers:squash')

@login_required
@user_passes_test(is_admin)
def squash(request):
    return render(request, 'customers/squash.html')

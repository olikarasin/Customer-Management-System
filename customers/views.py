# customers/views.py

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Customer, EmailReference, Technician, Contract, Credential
from .forms import CustomerForm, EmailReferenceForm, ContractForm, TechnicianForm, CredentialForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from accounts.models import UserProfile  # Import UserProfile
import random
import string

def main_login(request):
    return render(request, 'accounts/main_login.html')

def customer_list(request):
    query = request.GET.get('q', '')
    if query:
        customers = Customer.objects.filter(Q(name__icontains=query))
    else:
        customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            user = User.objects.create_user(username=customer.name, password='default_password')
            user_profile = UserProfile.objects.create(user=user, is_admin=False)  # Create UserProfile
            customer.user_profile = user_profile
            customer.save()
            emails = request.POST.getlist('emails')
            for email in emails:
                if email:
                    email_ref, created = EmailReference.objects.get_or_create(email=email)
                    customer.emails.add(email_ref)
            return redirect('customers:list')
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_create.html', {'form': form})

def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()
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

def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customers:list')
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})

def admin_dashboard(request):
    return redirect('customers:list')

def customer_dashboard(request):
    credentials = Credential.objects.filter(username=request.user.username)
    if credentials.exists():
        customer = credentials.first().customer
        timesheets = customer.timesheet_set.all()  # Assuming related name is 'timesheet_set'
        return render(request, 'customers/customer_dashboard.html', {'customer': customer, 'timesheets': timesheets})
    else:
        messages.error(request, "No customer information found.")
        return redirect('accounts:login')

def contract_list(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    contracts = Contract.objects.filter(customer=customer)
    return render(request, 'customers/contract_list.html', {'contracts': contracts, 'customer': customer})

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

def contract_delete(request, customer_id, pk):
    contract = get_object_or_404(Contract, pk=pk, customer_id=customer_id)
    if request.method == 'POST':
        contract.delete()
        return redirect('customers:contract_list', customer_id=customer_id)
    return render(request, 'customers/contract_confirm_delete.html', {'contract': contract, 'customer_id': customer_id})

def credential_list(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    credentials = Credential.objects.filter(customer=customer)
    return render(request, 'customers/credential_list.html', {'credentials': credentials, 'customer': customer})

def credential_create(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        form = CredentialForm(request.POST)
        if form.is_valid():
            credential = form.save(commit=False)
            credential.customer = customer
            credential.save()
            return redirect('customers:credential_list', customer_id=customer.id)
    else:
        form = CredentialForm()
    return render(request, 'customers/credential_create.html', {'form': form, 'customer': customer})

def credential_edit(request, customer_id, pk):
    credential = get_object_or_404(Credential, pk=pk, customer_id=customer_id)
    if request.method == 'POST':
        form = CredentialForm(request.POST, instance=credential)
        if form.is_valid():
            credential = form.save(commit=False)
            credential.save()
            return redirect('customers:credential_list', customer_id=customer_id)
    else:
        form = CredentialForm(instance=credential)
    return render(request, 'customers/credential_edit.html', {'form': form, 'customer_id': customer_id, 'credential': credential})

def credential_delete(request, customer_id, pk):
    credential = get_object_or_404(Credential, pk=pk, customer_id=customer_id)
    if request.method == 'POST':
        credential.delete()
        return redirect('customers:credential_list', customer_id=customer_id)
    return render(request, 'customers/credential_confirm_delete.html', {'credential': credential, 'customer_id': customer_id})

def technician_list(request):
    technicians = Technician.objects.all()
    return render(request, 'customers/technician_list.html', {'technicians': technicians})

def technician_create(request):
    if request.method == 'POST':
        form = TechnicianForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customers:technician_list')
    else:
        form = TechnicianForm()
    return render(request, 'customers/technician_create.html', {'form': form})

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

def reports(request):
    customers = Customer.objects.filter(status='Active')
    return render(request, 'customers/reports.html', {'customers': customers})

def update_renewal_status(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        customer.renewal_paid = not customer.renewal_paid
        customer.save()
    return redirect('customers:reports')

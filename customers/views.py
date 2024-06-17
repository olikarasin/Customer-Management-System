from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer, EmailReference, Technician, Contract
from .forms import CustomerForm, EmailReferenceForm, ContractForm, TechnicianForm
from django.db.models import Q

@login_required(login_url="/accounts/login/")
def customer_list(request):
    query = request.GET.get('q', '')
    if query:
        customers = Customer.objects.filter(Q(name__icontains=query))
    else:
        customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})

@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
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

@login_required
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

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customers:list')
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})

@login_required
def admin_dashboard(request):
    return redirect('customers:list')

@login_required
def customer_dashboard(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customer_dashboard.html', {'customers': customers})

@login_required
def contract_list(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    contracts = Contract.objects.filter(customer=customer)
    return render(request, 'customers/contract_list.html', {'contracts': contracts, 'customer': customer})

@login_required
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
def technician_list(request):
    technicians = Technician.objects.all()
    return render(request, 'customers/technician_list.html', {'technicians': technicians})

@login_required
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
def technician_delete(request, pk):
    technician = get_object_or_404(Technician, pk=pk)
    if request.method == 'POST':
        technician.delete()
        return redirect('customers:technician_list')
    return render(request, 'customers/technician_confirm_delete.html', {'technician': technician})

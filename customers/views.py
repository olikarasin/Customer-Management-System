from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer
from .forms import CustomerForm

@login_required(login_url="/accounts/login/")
def customer_list(request):
    query = request.GET.get('q', '')
    if query:
        customers = Customer.objects.filter(name__icontains=query)
    else:
        customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})

@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
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
            form.save()
            return redirect('customers:list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_edit.html', {'form': form})

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

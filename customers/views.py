from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer
from .forms import CustomerForm
from django.http import HttpResponseRedirect

@login_required(login_url="/accounts/login/")
def customer_list(request):
    if not request.user.userprofile.is_admin:
        return HttpResponseRedirect('/customer/dashboard/')  # Redirect non-admins
    customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})

@login_required(login_url="/accounts/login/")
def customer_create(request):
    if not request.user.userprofile.is_admin:
        return HttpResponseRedirect('/customer/dashboard/')  # Redirect non-admins
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customers:list')
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_create.html', {'form': form})

@login_required
def admin_dashboard(request):
    # This could just be a redirection to the customer list for simplicity
    return redirect('customers:list')

@login_required
def customer_dashboard(request):
    # For a simple customer dashboard, show a static or minimal page
    return render(request, 'customers/dashboard.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def main_login(request):
    return render(request, 'accounts/main_login.html')

def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('customers:list')  # Redirect to the customer list view
        else:
            messages.error(request, 'Invalid admin credentials')
    return render(request, 'accounts/admin_login.html')

def customer_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and not user.is_staff:
            login(request, user)
            return redirect('customers:customer_dashboard')
        else:
            messages.error(request, 'Invalid customer credentials')
    return render(request, 'accounts/customer_login.html')

def logout_view(request):
    logout(request)
    return redirect('accounts:main_login')

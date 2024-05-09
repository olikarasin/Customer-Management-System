from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile  # Ensure UserProfile is imported

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Assuming is_admin will be determined some other way, defaulting to False
            UserProfile.objects.create(user=user, is_admin=False)  # Create user profile when signing up
            login(request, user)
            return redirect_post_login(user)  # Redirect based on user type
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect_post_login(user)  # Redirect based on user type
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')  # More neutral redirection after logout

@login_required
def redirect_post_login(user):
    """Redirect users based on whether they are marked as admin in UserProfile."""
    if hasattr(user, 'userprofile') and user.userprofile.is_admin:
        return redirect('admin_dashboard')  # Adjust as needed for the admin dashboard URL
    else:
        return redirect('customer_dashboard')  # Adjust as needed for the customer dashboard URL

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.main_login, name='main_login'),
    path('admin_login/', views.admin_login_view, name='admin_login'),
    path('customer_login/', views.customer_login_view, name='customer_login'),
    path('logout/', views.logout_view, name='logout'),
]

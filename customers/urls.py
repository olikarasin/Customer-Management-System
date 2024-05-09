from django.urls import path
from .views import customer_list, customer_create
from .views import admin_dashboard, customer_dashboard

app_name = 'customers'

urlpatterns = [
    path('list/', customer_list, name='list'),
    path('create/', customer_create, name='create'),
    path('admin/dashboard/', admin_dashboard, name='admindash'),
    path('', customer_dashboard, name='dashboard'),
]

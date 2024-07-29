from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.customer_list, name='list'),
    path('create/', views.customer_create, name='create'),
    path('<int:pk>/edit/', views.customer_edit, name='edit'),
    path('<int:pk>/delete/', views.customer_delete, name='delete'),
    path('<int:customer_id>/contracts/', views.contract_list, name='contract_list'),
    path('<int:customer_id>/contracts/create/', views.contract_create, name='contract_create'),
    path('<int:customer_id>/contracts/<int:pk>/edit/', views.contract_edit, name='contract_edit'),
    path('<int:customer_id>/contracts/<int:pk>/delete/', views.contract_delete, name='contract_delete'),
    path('<int:customer_id>/contracts/<int:pk>/approve/', views.contract_approve, name='contract_approve'),
    path('technicians/', views.technician_list, name='technician_list'),
    path('technicians/create/', views.technician_create, name='technician_create'),
    path('technicians/<int:pk>/delete/', views.technician_delete, name='technician_delete'),
    path('<int:customer_id>/credentials/', views.credential_list, name='credential_list'),
    path('<int:customer_id>/credentials/create/', views.credential_create, name='credential_create'),
    path('<int:customer_id>/credentials/<int:pk>/edit/', views.credential_edit, name='credential_edit'),
    path('<int:customer_id>/credentials/<int:pk>/delete/', views.credential_delete, name='credential_delete'),
    path('generate_password/', views.generate_password, name='generate_password'),
    path('admin_dashboard/', views.customer_list, name='admin_dashboard'),  # Redirect to customer_list.html
    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('reports/', views.reports, name='reports'),
    path('update_renewal_status/<int:customer_id>/', views.update_renewal_status, name='update_renewal_status'),
    path('squash/', views.squash, name='squash'),
    path('squash/delete_timesheets_older_than_6_months/', views.delete_timesheets_older_than_6_months, name='delete_timesheets_older_than_6_months'),
    path('squash/delete_timesheets_of_inactive_customers/', views.delete_timesheets_of_inactive_customers, name='delete_timesheets_of_inactive_customers'),
    path('squash/delete_timesheets_in_range/', views.delete_timesheets_in_range, name='delete_timesheets_in_range'),
    path('squash/delete_timesheets_older_than_date/', views.delete_timesheets_older_than_date, name='delete_timesheets_older_than_date'),
]

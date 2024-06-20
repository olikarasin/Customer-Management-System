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
    path('technicians/', views.technician_list, name='technician_list'),
    path('technicians/create/', views.technician_create, name='technician_create'),
    path('technicians/<int:pk>/delete/', views.technician_delete, name='technician_delete'),
    path('<int:customer_id>/credentials/', views.credential_list, name='credential_list'),  # New line
    path('<int:customer_id>/credentials/create/', views.credential_create, name='credential_create'),  # New line
    path('<int:customer_id>/credentials/<int:pk>/edit/', views.credential_edit, name='credential_edit'),  # New line
    path('<int:customer_id>/credentials/<int:pk>/delete/', views.credential_delete, name='credential_delete'),  # New line
]

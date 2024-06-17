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
    path('technicians/', views.technician_list, name='technician_list'),  # Add this line
    path('technicians/create/', views.technician_create, name='technician_create'),  # Add this line
    path('technicians/<int:pk>/delete/', views.technician_delete, name='technician_delete'),  # Add this line
]

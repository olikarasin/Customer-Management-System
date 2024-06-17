from django.urls import path
from . import views

app_name = 'timesheets'

urlpatterns = [
    path('create/<int:customer_id>/', views.timesheet_create, name='create'),
    path('list/<int:customer_id>/', views.timesheets_list, name='list'),
    path('<int:pk>/edit/', views.timesheet_edit, name='edit'),
    path('<int:pk>/delete/', views.timesheet_delete, name='delete'),
    path('approve/<int:pk>/', views.approve_timesheet, name='approve'),
    path('upload_test/', views.upload_test, name='upload_test'),
]

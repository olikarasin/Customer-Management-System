from django.urls import path
from . import views

app_name = 'timesheets'

urlpatterns = [
    path('list/<int:customer_id>/', views.timesheets_list, name='list'),
    path('create/<int:customer_id>/', views.timesheet_create, name='create'),
    path('<int:pk>/edit/', views.timesheet_edit, name='edit'),
    path('<int:pk>/delete/', views.timesheet_delete, name='delete'),
    path('upload-test/', views.upload_test, name='upload-test'),
]

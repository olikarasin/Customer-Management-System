from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.customer_list, name='list'),
    path('create/', views.customer_create, name='create'),
    path('<int:pk>/edit/', views.customer_edit, name='edit'),
    path('<int:pk>/delete/', views.customer_delete, name='delete'),
    #path('<slug:slug>/', views.article_detail, name="detail") DO SUM LIKE THIS FOR CUSOTMER INFO
    # path('admin/dashboard/', admin_dashboard, name='admindash'),
    # path('', customer_dashboard, name='dashboard'),
]

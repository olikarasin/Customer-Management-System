from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from customers import views as customer_views

urlpatterns = [
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('admin/', admin.site.urls),
    path('customers/', include('customers.urls', namespace='customers')),
    path('', customer_views.main_login, name='main_login'),  # Main login page
    path('home/', customer_views.customer_list, name='home'),  # Define home URL
    path('timesheets/', include('timesheets.urls', namespace='timesheets')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

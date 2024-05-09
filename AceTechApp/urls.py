from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static # Allows to find/serve media files
from django.conf import settings 
from customers import views as customer_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/', include('customers.urls')),
    # path('about/', views.about),
    path('', customer_views.customer_list, name="home"),
    path('accounts/', include('accounts.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
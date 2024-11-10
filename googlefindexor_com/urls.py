
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
import home
from home import views 
from django.utils.translation import gettext_lazy as _


urlpatterns = [
    path('home/', include('home.urls')),
    path('', include('home.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
    path('jet/', include('jet.urls')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('company', views.company, name='company'),

    path('<slug:slug>', views.company_details, name='company_details'),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

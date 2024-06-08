
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
    

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

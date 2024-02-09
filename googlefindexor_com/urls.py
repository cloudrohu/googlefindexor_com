
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
import home
from home import views 
from order import views as OrderViews
from user import views as UserViews
from django.utils.translation import gettext_lazy as _


urlpatterns = [
    path('', include('home.urls')),
    path('home/', include('home.urls')),
    path('product/', include('product.urls')),
    path('order/', include('order.urls')),
    path('user/', include('user.urls'), name='user'),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),

    path('category/<int:id>/<slug:slug>', views.category_products, name='category_products'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('shopcart/', OrderViews.shopcart, name='shopcart'),
    path('login/', UserViews.login_form, name='login'),
    path('logout/', UserViews.logout_func, name='logout'),
    path('signup/', UserViews.signup_form, name='signup'),
    path('faq/', views.faq, name='faq'),
    path('ajaxcolor/', views.ajaxcolor, name='ajaxcolor'),  


    path(('about/'), views.aboutus, name='aboutus'),
    path(('service/'), views.SERVICES, name='service'),
    path(('furniture/'), views.furniture, name='furniture'),
    path(('contact/'), views.contactus, name='contactus'),
    path('search/', views.search, name='search'),
    path('search_auto/', views.search_auto, name='search_auto'),   

    path('category/<int:id>/<slug:slug>', views.category_products, name='category_products'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

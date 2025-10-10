from django.urls import path

from home.views import IndexView,DashboardView
from .import views 



urlpatterns = [
    path('', IndexView.as_view(), name='index'), 
    path('dashboard/', DashboardView.as_view(), name='dashboard'), 

    
]

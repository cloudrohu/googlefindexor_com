from django.urls import path

from home.views import IndexView,DashboardView,company_meeting_list, response_meeting_list
from .import views 



urlpatterns = [
    path('', IndexView.as_view(), name='index'), 
    path('dashboard/', DashboardView.as_view(), name='dashboard'), 
    # 🏢 Company Meetings Filter Views
    path('company-meetings/<str:filter_type>/', company_meeting_list, name='company_meeting_list'),

    # 📊 Response Meetings Filter Views
    path('response-meetings/<str:filter_type>/', response_meeting_list, name='response_meeting_list'),
    
]

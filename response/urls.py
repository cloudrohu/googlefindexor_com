# response/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Dashboard Views
    path('dashboard/', views.ResponseDashboardView.as_view(), {'status_slug': 'all'}, name='response_dashboard_all'), # /response/dashboard/
    path('dashboard/status/<slug:status_slug>/', views.ResponseDashboardView.as_view(), name='response_dashboard_status'),
    
    # CRUD Views
    path('add/', views.ResponseCreateView.as_view(), name='response_create'), # /response/add/
    path('<int:pk>/', views.ResponseDetailView.as_view(), name='response_detail'),
    path('<int:pk>/edit/', views.ResponseUpdateView.as_view(), name='response_update'),
    path('<int:pk>/delete/', views.ResponseDeleteView.as_view(), name='response_delete'),

    path('list/', views.ResponseListView.as_view(), name='response_list'),
    path('status/<str:status>/', views.ResponseStatusView.as_view(), name='response_status'),
    path('meetings/', views.ResponseMeetingsView.as_view(), name='response_meetings'),
    path('followups/', views.ResponseFollowupsView.as_view(), name='response_followups'),
]
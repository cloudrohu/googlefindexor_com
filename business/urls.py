from django.urls import path
from .import views

urlpatterns = [
    # COMPANY CRUD
    path('', views.CompanyListView.as_view(), name='company_list'),
    path('add/', views.CompanyCreateView.as_view(), name='company_add'),
    path('<int:pk>/<slug:slug>/', views.CompanyDetailView.as_view(), name='company_detail'),
    path('<int:pk>/edit/', views.CompanyUpdateView.as_view(), name='company_edit'),
    path('<int:pk>/delete/', views.CompanyDeleteView.as_view(), name='company_delete'),

    # COMMENTS (AJAX)
    path('<int:pk>/comment/add/', views.ajax_add_comment, name='business_ajax_add_comment'),

    # VOICE RECORDING (AJAX)
    path('<int:pk>/voice/add/', views.ajax_add_voice, name='business_ajax_add_voice'),
]

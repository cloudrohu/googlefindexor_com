from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect

from .models import Response, Meeting, Followup
from utility.models import Response_Status
from .forms import ResponseCreateForm, MeetingForm, FollowupForm


# =================================================================
#                       RESPONSE VIEWS
# =================================================================

class ResponseDashboardView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'response/dashboard.html'
    context_object_name = 'responses'
    # 👇 You can add logic for dashboard stats here later


class ResponseCreateView(LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseCreateForm
    template_name = 'response/response_create.html'
    success_url = reverse_lazy('response_dashboard_all')


class ResponseDetailView(LoginRequiredMixin, DetailView):
    model = Response
    template_name = 'response/response_detail.html'
    context_object_name = 'response'


class ResponseUpdateView(LoginRequiredMixin, UpdateView):
    model = Response
    form_class = ResponseCreateForm
    template_name = 'response/response_update.html'
    success_url = reverse_lazy('response_dashboard_all')


class ResponseDeleteView(LoginRequiredMixin, DeleteView):
    model = Response
    template_name = 'response/response_confirm_delete.html'
    success_url = reverse_lazy('response_dashboard_all')


# =================================================================
#                       FILTERED LIST VIEWS
# =================================================================

class ResponseListView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'dashboard/response/response_list.html'
    context_object_name = 'responses'


class ResponseStatusView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'response/response_status.html'
    context_object_name = 'responses'

    def get_queryset(self):
        status = self.kwargs.get('status')
        return Response.objects.filter(status=status)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_name'] = self.kwargs.get('status')
        return context


class ResponseMeetingsView(LoginRequiredMixin, ListView):
    model = Meeting
    template_name = 'response/response_meetings.html'
    context_object_name = 'meetings'


class ResponseFollowupsView(LoginRequiredMixin, ListView):
    model = Followup
    template_name = 'response/response_followups.html'
    context_object_name = 'followups'


class ResponseStatusView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'dashboard/response/response_status.html'
    context_object_name = 'responses'

    def get_queryset(self):
        status = self.kwargs.get('status')
        return Response.objects.filter(status=status)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_name'] = self.kwargs.get('status')
        return context

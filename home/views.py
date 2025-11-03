from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta
# ✅ Import both Meeting models correctly


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from business.models import Meeting as CompanyMeeting
from response.models import Meeting as ResponseMeeting
from business.forms import MeetingForm as BusinessMeetingForm
from response.forms import MeetingForm as ResponseMeetingForm


# 🏢 Company (Business) Meeting Edit View
@login_required
def edit_company_meeting(request, pk):
    meeting = get_object_or_404(CompanyMeeting, pk=pk)
    if request.method == 'POST':
        form = BusinessMeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.updated_by = request.user
            obj.save()
            messages.success(request, f"✅ Company Meeting #{meeting.id} updated successfully!")
            return redirect('company_meetings')  # Change this to your list view URL name
    else:
        form = BusinessMeetingForm(instance=meeting)

    return render(request, 'business/edit_meeting.html', {
        'form': form,
        'title': f"Edit Company Meeting #{meeting.id}",
        'meeting': meeting,
        'type': 'company'
    })


# 📊 Response Meeting Edit View
@login_required
def edit_response_meeting(request, pk):
    meeting = get_object_or_404(ResponseMeeting, pk=pk)
    if request.method == 'POST':
        form = ResponseMeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.updated_by = request.user
            obj.save()
            messages.success(request, f"✅ Response Meeting #{meeting.id} updated successfully!")
            return redirect('response_meetings')
    else:
        form = ResponseMeetingForm(instance=meeting)

    return render(request, 'response/edit_meeting.html', {
        'form': form,
        'title': f"Edit Response Meeting #{meeting.id}",
        'meeting': meeting,
        'type': 'response'
    })






class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Total counts for dashboard summary
        context['total_company_meetings'] = CompanyMeeting.objects.count()
        context['total_response_meetings'] = ResponseMeeting.objects.count()
        context['total_leads'] = 5240
        context['completed_responses'] = 1280
        context['pending_followups'] = 48
        context['total_revenue'] = "5.6M"

        # ✅ Meeting management data
        today = timezone.localdate()
        tomorrow = today + timedelta(days=1)
        valid_statuses = ['New Meeting', 'Re Meeting']

        # --- Company Meetings ---
        context['company_not_managed'] = CompanyMeeting.objects.filter(
            meeting_date__lt=today,
            status__in=valid_statuses
        )
        context['company_today'] = CompanyMeeting.objects.filter(
            meeting_date__date=today,
            status__in=valid_statuses
        )
        context['company_tomorrow'] = CompanyMeeting.objects.filter(
            meeting_date__date=tomorrow,
            status__in=valid_statuses
        )
        context['company_upcoming'] = CompanyMeeting.objects.filter(
            meeting_date__date__gt=tomorrow,
            status__in=valid_statuses
        )

        # --- Response Meetings ---
        context['response_not_managed'] = ResponseMeeting.objects.filter(
            meeting_date__lt=today,
            status__in=valid_statuses
        )
        context['response_today'] = ResponseMeeting.objects.filter(
            meeting_date__date=today,
            status__in=valid_statuses
        )
        context['response_tomorrow'] = ResponseMeeting.objects.filter(
            meeting_date__date=tomorrow,
            status__in=valid_statuses
        )
        context['response_upcoming'] = ResponseMeeting.objects.filter(
            meeting_date__date__gt=tomorrow,
            status__in=valid_statuses
        )

        return context


# 🏢 Filtered Company Meetings Page
def company_meeting_list(request, filter_type):
    today = timezone.localdate()
    tomorrow = today + timedelta(days=1)
    valid_status = ['New Meeting', 'Re Meeting']

    if filter_type == 'not-managed':
        meetings = CompanyMeeting.objects.filter(meeting_date__lt=today, status__in=valid_status)
        title = "❌ Not Managed Company Meetings"

    elif filter_type == 'today':
        meetings = CompanyMeeting.objects.filter(meeting_date__date=today, status__in=valid_status)
        title = "📅 Today's Company Meetings"

    elif filter_type == 'tomorrow':
        meetings = CompanyMeeting.objects.filter(meeting_date__date=tomorrow, status__in=valid_status)
        title = "🌤️ Tomorrow's Company Meetings"

    elif filter_type == 'upcoming':
        meetings = CompanyMeeting.objects.filter(meeting_date__date__gt=tomorrow, status__in=valid_status)
        title = "🚀 Upcoming Company Meetings"

    else:
        meetings = CompanyMeeting.objects.none()
        title = "No Meetings Found"

    return render(request, 'business/meeting_list.html', {
        'meetings': meetings,
        'title': title,
        'type': 'company',
    })


# 📊 Filtered Response Meetings Page
def response_meeting_list(request, filter_type):
    today = timezone.localdate()
    tomorrow = today + timedelta(days=1)
    valid_status = ['New Meeting', 'Re Meeting']

    if filter_type == 'not-managed':
        meetings = ResponseMeeting.objects.filter(meeting_date__lt=today, status__in=valid_status)
        title = "❌ Not Managed Response Meetings"

    elif filter_type == 'today':
        meetings = ResponseMeeting.objects.filter(meeting_date__date=today, status__in=valid_status)
        title = "📅 Today's Response Meetings"

    elif filter_type == 'tomorrow':
        meetings = ResponseMeeting.objects.filter(meeting_date__date=tomorrow, status__in=valid_status)
        title = "🌤️ Tomorrow's Response Meetings"

    elif filter_type == 'upcoming':
        meetings = ResponseMeeting.objects.filter(meeting_date__date__gt=tomorrow, status__in=valid_status)
        title = "🚀 Upcoming Response Meetings"

    else:
        meetings = ResponseMeeting.objects.none()
        title = "No Meetings Found"

    return render(request, 'response/meeting_list.html', {
        'meetings': meetings,
        'title': title,
        'type': 'response',
    })



# ✅ Optional: Separate IndexView if you need landing dashboard
class IndexView(LoginRequiredMixin, TemplateView):
    """
    Displays summarized key performance indicators (KPIs)
    on the main index (home) page.
    """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Dummy data until models are ready
        context.update({
            'total_leads': 5240,
            'completed_responses': 1280,
            'pending_followups': 48,
            'total_revenue': "5.6M",
        })

        # Example: when CRM models are connected
        # from crm.models import Lead, Response
        # context['total_leads'] = Lead.objects.count()
        # context['completed_responses'] = Response.objects.filter(status='completed').count()

        return context

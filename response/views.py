# ===========================================================
# response/views.py (Final Polished – Added Followups Support)
# ===========================================================
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.files import File

import os

from .models import Response, Meeting, Followup, Comment, VoiceRecording
from .forms import (
    ResponseForm,        # ✅ CORRECT
    MeetingForm,
    FollowupForm,
    CommentForm,
    VoiceRecordingForm,
)

# =================================================================
#                       AJAX VOICE UPLOAD
# =================================================================

@csrf_exempt
@require_POST
def ajax_add_voice(request, pk):
    """Upload & compress voice note using ffmpeg (via pydub)."""
    response = get_object_or_404(Response, pk=pk)
    if 'file' not in request.FILES:
        return JsonResponse({'success': False, 'error': 'No file uploaded'})

    file = request.FILES['file']
    voice_obj = VoiceRecording.objects.create(
        response=response,
        file=file,
        uploaded_by=request.user
    )

    original_path = voice_obj.file.path
    compressed_path = original_path.rsplit('.', 1)[0] + "_compressed.mp3"

    try:
        if not original_path.lower().endswith(".mp3"):
            audio = AudioSegment.from_file(original_path)
            audio = audio.set_frame_rate(22050).set_channels(1)
            audio.export(compressed_path, format="mp3", bitrate="64k")

            with open(compressed_path, 'rb') as f:
                voice_obj.file.save(os.path.basename(compressed_path), File(f), save=True)

            os.remove(original_path)
            os.remove(compressed_path)

        return JsonResponse({
            'success': True,
            'file_url': voice_obj.file.url,
            'uploaded_by': voice_obj.uploaded_by.username,
            'uploaded_at': voice_obj.uploaded_at.strftime('%d %b %Y %H:%M')
        })
    except Exception as e:
        print("Voice compression error:", e)
        return JsonResponse({
            'success': True,
            'file_url': voice_obj.file.url,
            'uploaded_by': voice_obj.uploaded_by.username,
            'uploaded_at': voice_obj.uploaded_at.strftime('%d %b %Y %H:%M'),
            'warning': 'Compression failed, original file used'
        })


# =================================================================
#                       RESPONSE VIEWS
# =================================================================

class ResponseListView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'dashboard/response/response_list.html'
    context_object_name = 'responses'
    paginate_by = 20

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        return response


class ResponseStatusView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'dashboard/response/response_status.html'
    context_object_name = 'responses'
    paginate_by = 20

    def get_queryset(self):
        status = self.kwargs.get('status')
        return Response.objects.filter(status=status).order_by('-create_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_name'] = self.kwargs.get('status')
        return context


class ResponseCreateView(LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseForm
    template_name = 'dashboard/response/response_create.html'
    success_url = reverse_lazy('response_list')


class ResponseDetailView(LoginRequiredMixin, DetailView):
    model = Response
    template_name = 'dashboard/response/response_detail.html'
    context_object_name = 'response'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = self.get_object()
        context['meetings'] = Meeting.objects.filter(response=response)
        context['followups'] = Followup.objects.filter(response=response)
        context['comments'] = Comment.objects.filter(response=response).order_by('-create_at')
        context['voice_recordings'] = VoiceRecording.objects.filter(response=response).order_by('-uploaded_at')

        # Inline forms
        context['comment_form'] = CommentForm()
        context['meeting_form'] = MeetingForm()
        context['followup_form'] = FollowupForm()
        context['voice_form'] = VoiceRecordingForm()
        return context


class ResponseUpdateView(LoginRequiredMixin, UpdateView):
    model = Response
    form_class = ResponseForm
    template_name = 'dashboard/response/response_update.html'

    def get_success_url(self):
        return reverse_lazy('response_detail', kwargs={'pk': self.object.pk})


class ResponseDeleteView(LoginRequiredMixin, DeleteView):
    model = Response
    template_name = 'dashboard/response/response_confirm_delete.html'
    success_url = reverse_lazy('response_list')


# =================================================================
#                       MEETING VIEWS
# =================================================================

class MeetingListView(LoginRequiredMixin, ListView):
    model = Meeting
    template_name = 'dashboard/meeting/meeting_list.html'
    context_object_name = 'meetings'
    paginate_by = 20


class MeetingCreateView(LoginRequiredMixin, CreateView):
    model = Meeting
    form_class = MeetingForm
    template_name = 'dashboard/meeting/meeting_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('response_detail', kwargs={'pk': self.object.response.pk})


# =================================================================
#                       FOLLOWUP VIEWS
# =================================================================

class FollowupListView(LoginRequiredMixin, ListView):
    model = Followup
    template_name = 'dashboard/followup/followup_list.html'
    context_object_name = 'followups'
    paginate_by = 20


class FollowupCreateView(LoginRequiredMixin, CreateView):
    model = Followup
    form_class = FollowupForm
    template_name = 'dashboard/followup/followup_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('response_detail', kwargs={'pk': self.object.response.pk})


# =================================================================
#                       AJAX COMMENT & STATUS
# =================================================================

@csrf_exempt
@require_POST
def ajax_add_comment(request, pk):
    """Adds a new comment via AJAX."""
    response = get_object_or_404(Response, pk=pk)
    comment_text = request.POST.get('comment')
    if comment_text and comment_text.strip():
        comment = Comment.objects.create(
            response=response,
            comment=comment_text.strip(),
            created_by=request.user
        )
        return JsonResponse({
            'success': True,
            'comment': comment.comment,
            'created_by': comment.created_by.username,
            'created_at': comment.create_at.strftime('%d %b %Y %H:%M')
        })
    return JsonResponse({'success': False, 'error': 'Comment cannot be empty'})


@csrf_exempt
@require_POST
def ajax_update_status(request, pk):
    """Updates Response status via AJAX."""
    try:
        response = Response.objects.get(pk=pk)
        new_status = request.POST.get('status')

        if new_status not in dict(Response.STATUS_CHOICES):
            return JsonResponse({'success': False, 'error': 'Invalid status value'})

        response.status = new_status
        response.save(update_fields=['status'])

        return JsonResponse({
            'success': True,
            'new_status': response.status,
            'new_status_display': response.get_status_display()
        })
    except Response.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Response not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

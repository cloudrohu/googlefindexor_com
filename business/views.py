from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Company, Comment, VoiceRecording, Visit
from .forms import CompanyForm, CommentForm, VoiceRecordingForm, VisitForm

# Optional audio compression
import os
from django.core.files import File


# =====================================================
# 📄 COMPANY LIST VIEW  (Business List)
# =====================================================
class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'business/company_list.html'
    context_object_name = 'companies'
    paginate_by = 5

    def get_queryset(self):
        return Company.objects.select_related('city', 'locality', 'category').order_by('-create_at')


# =====================================================
# 📄 COMPANY STATUS FILTER VIEW (optional like response/status/<status>/)
# =====================================================
class CompanyStatusListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'business/company_list.html'
    context_object_name = 'companies'
    paginate_by = 5

    def get_queryset(self):
        status = self.kwargs.get('status')
        return Company.objects.filter(status=status).select_related('city', 'locality', 'category').order_by('-create_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.kwargs.get('status')
        return context


# =====================================================
# 📝 COMPANY DETAIL VIEW
# =====================================================
class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = Company
    template_name = 'business/company_detail.html'
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.get_object()
        context['comments'] = Comment.objects.filter(company=company).order_by('-create_at')
        context['voice_recordings'] = VoiceRecording.objects.filter(company=company).order_by('-uploaded_at')
        context['visits'] = Visit.objects.filter(company=company).order_by('-uploaded_at')
        context['comment_form'] = CommentForm()
        context['voice_form'] = VoiceRecordingForm()
        context['visit_form'] = VisitForm()
        return context


# =====================================================
# ➕ COMPANY CREATE VIEW
# =====================================================
class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'business/company_form.html'
    success_url = reverse_lazy('company_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


# =====================================================
# ✏️ COMPANY UPDATE VIEW
# =====================================================
class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'business/company_form.html'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('company_detail', kwargs={'pk': self.object.pk, 'slug': self.object.slug})


# =====================================================
# 🗑 COMPANY DELETE VIEW
# =====================================================
class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = Company
    template_name = 'business/company_confirm_delete.html'
    success_url = reverse_lazy('company_list')


# =====================================================
# 💬 AJAX: Add Comment
# =====================================================
@csrf_exempt
@require_POST
@login_required
def ajax_add_comment(request, pk):
    company = get_object_or_404(Company, pk=pk)
    comment_text = request.POST.get('comment')
    if comment_text and comment_text.strip():
        comment = Comment.objects.create(
            company=company,
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


# =====================================================
# 🎤 AJAX: Add Voice
# =====================================================
@csrf_exempt
@require_POST
@login_required
def ajax_add_voice(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if 'file' not in request.FILES:
        return JsonResponse({'success': False, 'error': 'No file uploaded'})

    file = request.FILES['file']
    voice_obj = VoiceRecording.objects.create(
        company=company,
        file=file,
        uploaded_by=request.user
    )

    original_path = voice_obj.file.path
    compressed_path = original_path.rsplit('.', 1)[0] + "_compressed.mp3"

    try:
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
        print("Compression error:", e)
        return JsonResponse({
            'success': True,
            'file_url': voice_obj.file.url,
            'uploaded_by': voice_obj.uploaded_by.username,
            'uploaded_at': voice_obj.uploaded_at.strftime('%d %b %Y %H:%M'),
            'warning': 'Compression failed, original file used'
        })


# =====================================================
# ⚡ AJAX: Update Status
# =====================================================
@csrf_exempt
@require_POST
@login_required
def ajax_update_status(request, pk):
    company = get_object_or_404(Company, pk=pk)
    new_status = request.POST.get('status')
    if new_status:
        company.status = new_status
        company.save(update_fields=['status'])
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid status'})


# =====================================================
# 📝 AJAX: Add Visit
# =====================================================
@csrf_exempt
@require_POST
@login_required
def ajax_add_visit(request, pk):
    company = get_object_or_404(Company, pk=pk)
    form = VisitForm(request.POST)
    if form.is_valid():
        visit = form.save(commit=False)
        visit.company = company
        visit.uploaded_by = request.user
        visit.save()
        return JsonResponse({
            'success': True,
            'visit_for': visit.visit_for,
            'visit_type': visit.visit_type,
            'visit_status': visit.visit_status,
            'comment': visit.comment or '',
            'uploaded_at': visit.uploaded_at.strftime('%d %b %Y %H:%M')
        })
    return JsonResponse({'success': False, 'errors': form.errors})

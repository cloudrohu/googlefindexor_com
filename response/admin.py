from django.contrib import admin
from django.utils.html import format_html
from .models import Response, Meeting, Comment, VoiceRecording



from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import path
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect


# 🎧 Quick Upload Form
class VoiceRecordingQuickForm(forms.ModelForm):
    class Meta:
        model = VoiceRecording
        fields = ['file', 'note']

# ------------------------------
#  Inlines
# ------------------------------
class MeetingInline(admin.TabularInline):
    model = Meeting
    extra = 1
    show_change_link = True
    fields = ('status', 'meeting_date', 'assigned_to', 'comment')


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ('comment', 'create_at', 'update_at')
    readonly_fields = ('create_at', 'update_at')


class VoiceRecordingInline(admin.TabularInline):
    model = VoiceRecording
    extra = 1
    fields = ('file', 'note', 'audio_player', 'uploaded_by', 'uploaded_at')
    readonly_fields = ('audio_player', 'uploaded_by', 'uploaded_at')

    def audio_player(self, obj):
        if obj.file:
            return format_html(
                '''
                <audio controls style="width: 200px;">
                    <source src="{}" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
                ''',
                obj.file.url
            )
        return "(No file yet)"
    audio_player.short_description = "Preview 🎧"


# ------------------------------
#  Response Admin
# ------------------------------
@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'contact_no',
        'status',
        'meeting_follow',
        'assigned_to',
        'business_name',
        'city',
        'locality_city',
        'comments_preview',
        'voice_preview',
    )
    list_filter = ('status',
                   'business_name',
                    'city',
                    'locality_city',)
    search_fields = ('contact_no', 'business_name')
    list_editable = (
        'status',
        'meeting_follow',
        'assigned_to',
        'business_name',
        'city',
        'locality_city',
    )
    ordering = ['-create_at']
    inlines = [MeetingInline, CommentInline, VoiceRecordingInline]
    readonly_fields = ('create_at', 'update_at',  )
    list_per_page = 10

    # 📝 Meeting Date preview
    def meeting_date_preview(self, obj):
        # Latest meeting for that response
        meeting = obj.meeting_set.order_by('-meeting_date').first()
        if meeting and meeting.meeting_date:
            return meeting.meeting_date.strftime('%b %d, %Y, %I:%M %p')
        return "-"
    meeting_date_preview.short_description = "Meeting Date & Time"

    # 📝 Comment preview (last comment)
    def comments_preview(self, obj):
        last_comment = obj.comments.order_by('-create_at').first()
        if last_comment:
            return (last_comment.comment[:40] + "…") if len(last_comment.comment) > 40 else last_comment.comment
        return "-"
    comments_preview.short_description = "Latest Comment"

    # 📝 Voice Recording preview (count or file icon)
    def voice_preview(self, obj):
        count = obj.recordings.count()
        if count > 0:
            return format_html('<span style="color:#007bff;">🎤 {} file(s)</span>', count)
        return "-"
    voice_preview.short_description = "Voice Notes"

    def voice_preview(self, obj):
        latest = obj.recordings.order_by('-uploaded_at').first()
        if latest and latest.file:
            return format_html(
                '''
                <audio controls style="width: 200px;">
                    <source src="{}" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
                ''',
                latest.file.url
            )
        return "-"


     # 🎤 Quick Add Button Column
    def quick_add_recording_button(self, obj):
        return format_html(
            '<a class="button" href="quick-add-recording/{}/">🎧 Quick Add</a>',
            obj.id
        )
    quick_add_recording_button.short_description = "Quick Voice Upload"

    # 🧭 Custom URL for modal form
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'quick-add-recording/<int:response_id>/',
                self.admin_site.admin_view(self.quick_add_recording_view),
                name='quick_add_recording',
            ),
        ]
        return custom_urls + urls

    # 🎤 View to handle quick upload
    def quick_add_recording_view(self, request, response_id):
        response_obj = Response.objects.get(pk=response_id)
        if request.method == 'POST':
            form = VoiceRecordingQuickForm(request.POST, request.FILES)
            if form.is_valid():
                recording = form.save(commit=False)
                recording.response = response_obj
                recording.uploaded_by = request.user
                recording.save()
                messages.success(request, "✅ Voice recording uploaded successfully!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            form = VoiceRecordingQuickForm()

        context = dict(
            self.admin_site.each_context(request),
            form=form,
            response_obj=response_obj,
        )
        return render(request, 'admin/quick_add_voice_recording.html', context)

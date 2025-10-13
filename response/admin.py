from django.contrib import admin
from django.utils.html import format_html
from .models import Response, Meeting, Comment, VoiceRecording

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
    fields = ('file', 'note', 'uploaded_at', 'uploaded_by')
    readonly_fields = ('uploaded_at', 'uploaded_by')


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

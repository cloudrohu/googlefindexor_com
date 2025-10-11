from django.contrib import admin
from django import forms
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Response, Meeting, Comment, VoiceRecording


# ------------------------------
#  Import Export Resources
# ------------------------------
class ResponseResource(resources.ModelResource):
    class Meta:
        model = Response
        fields = (
            "id", "status", "contact_persone", "contact_no",
            "meeting_follow", "business_name", "business_category",
            "locality_city", "city", "created_by", "updated_by",
            "create_at", "update_at"
        )


class MeetingResource(resources.ModelResource):
    class Meta:
        model = Meeting
        fields = ("id", "response", "status", "meeting_date", "assigned_to", "comment")


class CommentResource(resources.ModelResource):
    class Meta:
        model = Comment
        fields = ("id", "response", "comment", "created_by", "updated_by", "create_at", "update_at")


class VoiceRecordingResource(resources.ModelResource):
    class Meta:
        model = VoiceRecording
        fields = ("id", "response", "file", "uploaded_by", "uploaded_at", "note")


# ------------------------------
#  Inlines
# ------------------------------
class MeetingInline(admin.TabularInline):
    model = Meeting
    extra = 1
    show_change_link = True


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    show_change_link = True


class VoiceRecordingInline(admin.TabularInline):
    model = VoiceRecording
    extra = 1
    show_change_link = True
    readonly_fields = ('uploaded_at',)


# ------------------------------
#  Response Admin
# ------------------------------
class ResponseAdminForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = '__all__'


class ResponseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ResponseResource
    form = ResponseAdminForm
    exclude = ['created_by', 'updated_by']

    list_display = [
        'get_mr_id',        
        'status',
        'contact_no',

        'business_name',
        'contact_persone',
        'meeting_follow',
        'city',
        'locality_city',
        'update_at',
        'updated_by',
        'create_at'
    ]
    list_filter = ['status', 'city', 'locality_city', 'business_category']
    search_fields = ['id', 'contact_no', 'business_name', 'contact_persone']
    list_per_page = 20

    inlines = [MeetingInline, CommentInline, VoiceRecordingInline]

    def get_mr_id(self, obj):
        return f"MR{obj.id}"
    get_mr_id.short_description = "ID"


# ------------------------------
#  Other Admins
# ------------------------------
@admin.register(Meeting)
class MeetingAdmin(ImportExportModelAdmin):
    resource_class = MeetingResource
    list_display = ('id', 'response', 'status', 'meeting_date', 'assigned_to')
    list_filter = ('status',)
    search_fields = ('response__business_name', 'response__contact_no')


@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):
    resource_class = CommentResource
    list_display = ('id', 'response', 'comment', 'created_by', 'create_at')
    search_fields = ('response__id', 'comment')


@admin.register(VoiceRecording)
class VoiceRecordingAdmin(ImportExportModelAdmin):
    resource_class = VoiceRecordingResource
    list_display = ('id', 'response', 'file', 'uploaded_by', 'uploaded_at', 'note')
    search_fields = ('response__id', 'note')


# Register Response last to ensure inlines work
admin.site.register(Response, ResponseAdmin)

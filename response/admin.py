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
    fields = ('comment', 'create_at', 'update_at')
    readonly_fields = ('create_at', 'update_at')


class VoiceRecordingInline(admin.TabularInline):
    model = VoiceRecording
    extra = 1
    fields = ('file', 'note', 'uploaded_at')
    readonly_fields = ('uploaded_at',)


# ------------------------------
#  Response Admin
# ------------------------------
class ResponseAdminForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = '__all__'


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'contact_no', 'status', 'assigned_to', 'create_at', 'update_at')
    list_filter = ('status', 'create_at', 'update_at')
    search_fields = ('contact_no', 'business_name')
    inlines = [MeetingInline, CommentInline, VoiceRecordingInline]
    readonly_fields = ('create_at', 'update_at', 'created_by', 'updated_by')
    ordering = ['-create_at']

    fieldsets = (
        ("Response Info", {
            "fields": (
                "status", "contact_no", "contact_persone", "meeting_follow",
                "business_name", "business_category", "requirement_types", "city", "locality_city", "assigned_to"
            )
        }),
        ("Meta Info", {
            "fields": ("create_at", "update_at", "created_by", "updated_by")
        }),
    )

    # 👇 Auto-fill created_by & updated_by
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    # 👇 Auto-fill created_by / updated_by / uploaded_by for inlines
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            # Comment inline
            if hasattr(obj, 'created_by') and not obj.created_by:
                obj.created_by = request.user
            if hasattr(obj, 'updated_by'):
                obj.updated_by = request.user

            # VoiceRecording inline
            if hasattr(obj, 'uploaded_by') and not obj.uploaded_by:
                obj.uploaded_by = request.user

            obj.save()
        formset.save_m2m()

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

from django.contrib import admin
from .models import Staff, Response, Meeting, Followup, Comment, VoiceRecording


# ===========================
#  Auto Set User Mixin
# ===========================
class AutoUserAdminMixin:
    """Automatically sets created_by / updated_by / uploaded_by in admin."""

    def save_model(self, request, obj, form, change):
        # Set creator once
        if not change or not obj.pk:
            if hasattr(obj, 'created_by') and not obj.created_by:
                obj.created_by = request.user
        # Always update modifier
        if hasattr(obj, 'updated_by'):
            obj.updated_by = request.user
        # For models like VoiceRecording
        if hasattr(obj, 'uploaded_by') and not obj.uploaded_by:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        """Ensure inline models also get auto-filled."""
        instances = formset.save(commit=False)
        for instance in instances:
            if hasattr(instance, 'created_by') and not instance.created_by:
                instance.created_by = request.user
            if hasattr(instance, 'updated_by'):
                instance.updated_by = request.user
            if hasattr(instance, 'uploaded_by') and not instance.uploaded_by:
                instance.uploaded_by = request.user
            instance.save()
        formset.save_m2m()

    def get_readonly_fields(self, request, obj=None):
        """
        Show audit fields readonly during edit, but not block adding new records.
        """
        ro_fields = getattr(self, 'readonly_fields', [])
        if obj:  # Edit mode
            return ro_fields + ('created_by', 'updated_by', 'create_at', 'update_at')
        else:  # Add mode
            return ro_fields + ('create_at', 'update_at')

    def render_change_form(self, request, context, *args, **kwargs):
        """Pre-fill created_by / updated_by with current user in form UI."""
        form = context['adminform'].form
        if not form.initial.get('created_by'):
            form.initial['created_by'] = request.user
        if not form.initial.get('updated_by'):
            form.initial['updated_by'] = request.user
        return super().render_change_form(request, context, *args, **kwargs)


# ===========================
#  Inline Models (Now Add Works)
# ===========================
class MeetingInline(admin.TabularInline):
    model = Meeting
    extra = 1  # ✅ allows "Add another"
    fields = ('status', 'meeting_date', 'assigned_to', 'comment')
    exclude = ('created_by', 'updated_by', 'create_at', 'update_at')  # ✅ hidden but auto-saved
    show_change_link = True


class FollowupInline(admin.TabularInline):
    model = Followup
    extra = 1
    fields = ('status', 'followup_date', 'assigned_to', 'comment')
    exclude = ('created_by', 'updated_by', 'create_at', 'update_at')
    show_change_link = True


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ('comment',)
    exclude = ('created_by', 'updated_by', 'create_at', 'update_at')
    show_change_link = True


class VoiceRecordingInline(admin.TabularInline):
    model = VoiceRecording
    extra = 1
    fields = ('file', 'note')
    exclude = ('uploaded_by', 'uploaded_at')
    show_change_link = True

@admin.register(Response)
class ResponseAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    """Main admin for Responses with Jazzmin tabs and working inline add forms"""

    # ✅ Enable Jazzmin tabbed layout
    tabs = True

    list_display = (
        'id', 'contact_no', 'contact_persone', 'business_name', 'status',
        'city', 'locality_city', 'assigned_to', 'create_at'
    )
    list_filter = ('status', 'city', 'assigned_to')
    search_fields = ('contact_no', 'business_name', 'contact_persone')

    readonly_fields = ('create_at', 'update_at')

    # ✅ Default fieldsets (form fields shown on first tabs)
    fieldsets = (
        ('📞 Contact Information', {
            'fields': ('contact_no', 'contact_persone', 'assigned_to', 'status')
        }),
        ('🏢 Business Details', {
            'fields': (
                'business_name', 'business_category', 'requirement_types',
                'city', 'locality_city'
            )
        }),
        ('🕓 Audit Trail', {
            'fields': ('created_by', 'updated_by', 'create_at', 'update_at')
        }),
    )

    # ✅ Map fieldsets to Jazzmin tabs
    tab_fieldsets = (
        ('📞 Contact Information', 'Contact Information'),
        ('🏢 Business Details', 'Business Details'),
        ('🕓 Audit Trail', 'Audit Trail'),
    )

    # ✅ This is the most important part
    # Inline tabs are declared separately for Jazzmin
    tab_inlines = [
        ('🗓 Meetings', MeetingInline),
        ('🔁 Followups', FollowupInline),
        ('💬 Comments', CommentInline),
        ('🎤 Voice Recordings', VoiceRecordingInline),
    ]

    # ✅ Normal inlines list (Django requires this to register)
    inlines = [MeetingInline, FollowupInline, CommentInline, VoiceRecordingInline]

    # ✅ Optional: Fancy tab icons (Font Awesome)
    tab_icons = {
        '📞 Contact Information': 'fas fa-phone',
        '🏢 Business Details': 'fas fa-building',
        '🕓 Audit Trail': 'fas fa-clock',
        '🗓 Meetings': 'fas fa-calendar-check',
        '🔁 Followups': 'fas fa-sync',
        '💬 Comments': 'fas fa-comments',
        '🎤 Voice Recordings': 'fas fa-microphone'
    }

# ===========================
#  Sub Models Admins
# ===========================
@admin.register(Meeting)
class MeetingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'response', 'response_contact', 'response_business', 'status', 'meeting_date', 'assigned_to', 'create_at')
    list_filter = ('status', 'assigned_to')
    search_fields = ('response__contact_no', 'response__business_name')
    readonly_fields = ('create_at', 'update_at', 'created_by', 'updated_by')

    def response_contact(self, obj):
        return obj.response.contact_no
    response_contact.short_description = "Contact No"

    def response_business(self, obj):
        return obj.response.business_name
    response_business.short_description = "Business"


@admin.register(Followup)
class FollowupAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'response', 'response_contact', 'response_business', 'status', 'followup_date', 'assigned_to', 'create_at')
    list_filter = ('status', 'assigned_to')
    search_fields = ('response__contact_no', 'response__business_name')
    readonly_fields = ('create_at', 'update_at', 'created_by', 'updated_by')

    def response_contact(self, obj):
        return obj.response.contact_no
    response_contact.short_description = "Contact No"

    def response_business(self, obj):
        return obj.response.business_name
    response_business.short_description = "Business"


@admin.register(Comment)
class CommentAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'response', 'response_contact', 'response_business', 'comment', 'created_by', 'create_at')
    search_fields = ('response__contact_no', 'comment')
    readonly_fields = ('create_at', 'update_at', 'created_by', 'updated_by')

    def response_contact(self, obj):
        return obj.response.contact_no if obj.response else None
    response_contact.short_description = "Contact No"

    def response_business(self, obj):
        return obj.response.business_name if obj.response else None
    response_business.short_description = "Business"


@admin.register(VoiceRecording)
class VoiceRecordingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'response', 'response_contact', 'response_business', 'note', 'uploaded_by', 'uploaded_at')
    search_fields = ('response__contact_no', 'note')
    readonly_fields = ('uploaded_by', 'uploaded_at')

    def response_contact(self, obj):
        return obj.response.contact_no if obj.response else None
    response_contact.short_description = "Contact No"

    def response_business(self, obj):
        return obj.response.business_name if obj.response else None
    response_business.short_description = "Business"


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')

from django.contrib import admin
from .models import (
    Company, Meeting, Followup, Comment, VoiceRecording, Visit,
    Approx, SocialLink, Error, Images, Faq
)
from response.models import Staff


# ============================================================
# Auto User Mixin
# ============================================================
class AutoUserAdminMixin:
    """Automatically sets created_by / updated_by / uploaded_by in admin."""

    def save_model(self, request, obj, form, change):
        if not change or not obj.pk:
            if hasattr(obj, 'created_by') and not obj.created_by:
                obj.created_by = request.user
        if hasattr(obj, 'updated_by'):
            obj.updated_by = request.user
        if hasattr(obj, 'uploaded_by') and not obj.uploaded_by:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
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
        ro_fields = getattr(self, 'readonly_fields', [])
        if obj:
            return ro_fields + ('created_by', 'updated_by', 'create_at', 'update_at')
        return ro_fields + ('create_at', 'update_at')


# ============================================================
# Company Info Mixin (for Inlines)
# ============================================================
class CompanyInfoMixin:
    """Show key Company details inside inline models."""

    def company_name(self, obj):
        return obj.company.company_name if obj.company else None
    company_name.short_description = "Company Name"

    def company_city(self, obj):
        return obj.company.city if obj.company else None
    company_city.short_description = "City"

    def company_locality(self, obj):
        return obj.company.locality if obj.company else None
    company_locality.short_description = "Locality"

    def company_contact(self, obj):
        return obj.company.contact_no if obj.company else None
    company_contact.short_description = "Contact No"

    def company_assigned_to(self, obj):
        return obj.company.assigned_to if obj.company else None
    company_assigned_to.short_description = "Assigned To"


# ============================================================
# Inline Models
# ============================================================
class MeetingInline(CompanyInfoMixin, admin.TabularInline):
    model = Meeting
    extra = 1
    fields = ('company_name', 'company_city', 'company_locality', 'company_contact',
              'status', 'meeting_date', 'assigned_to', 'comment')
    readonly_fields = ('company_name', 'company_city', 'company_locality', 'company_contact')
    exclude = ('created_by', 'updated_by', 'create_at', 'update_at')
    show_change_link = True


class FollowupInline(CompanyInfoMixin, admin.TabularInline):
    model = Followup
    extra = 1
    fields = ('company_name', 'company_city', 'company_locality', 'company_contact',
              'status', 'followup_date', 'assigned_to', 'comment')
    readonly_fields = ('company_name', 'company_city', 'company_locality', 'company_contact')
    exclude = ('created_by', 'updated_by', 'create_at', 'update_at')
    show_change_link = True


class CommentInline(CompanyInfoMixin, admin.TabularInline):
    model = Comment
    extra = 1
    fields = ('company_name', 'company_city', 'company_locality', 'company_contact', 'comment')
    readonly_fields = ('company_name', 'company_city', 'company_locality', 'company_contact')
    exclude = ('created_by', 'updated_by', 'create_at', 'update_at')
    show_change_link = True


class VoiceRecordingInline(CompanyInfoMixin, admin.TabularInline):
    model = VoiceRecording
    extra = 1
    fields = ('company_name', 'company_city', 'company_locality', 'company_contact', 'file')
    readonly_fields = ('company_name', 'company_city', 'company_locality', 'company_contact')
    exclude = ('uploaded_by', 'uploaded_at')
    show_change_link = True


class VisitInline(CompanyInfoMixin, admin.TabularInline):
    model = Visit
    extra = 1
    fields = ('company_name', 'company_city', 'company_locality', 'company_contact',
              'visit_for', 'visit_type', 'visit_status', 'comment', 'uploaded_by')
    readonly_fields = ('company_name', 'company_city', 'company_locality', 'company_contact')
    exclude = ('uploaded_at',)
    show_change_link = True


# ============================================================
# Company Admin (Main)
# ============================================================
@admin.register(Company)
class CompanyAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = (
        'get_bc_id', 'company_name', 'contact_no',  'status','followup_meeting', 'locality', 'address',
        'contact_person', 'category', 'city',  'assigned_to',
        'create_at', 'created_by', 'update_at', 'updated_by'
    )

    def get_bc_id(self, obj):
        """Show BC + zero-padded ID"""
        if obj.id:
            return f"BC{str(obj.id).zfill(3)}"
        return "-"
    get_bc_id.short_description = "Company ID"

    

    def get_bc_id(self, obj):
        """Display MR + zero-padded ID."""
        return f"BC{str(obj.id).zfill(3)}"    

    get_bc_id.short_description = "Company ID"  # 👈 Column header name

    list_filter = ('status', 'city', 'assigned_to', 'category','locality','status','followup_meeting',)
    search_fields = ('company_name', 'contact_person', 'contact_no',)
    list_editable = ('status','followup_meeting')
    readonly_fields = ('create_at', 'update_at', 'slug', 'image_tag')

    fieldsets = (
        ('🏢 Company Information', {
            'fields': (
                'company_name', 'category', 'city', 'locality', 'address', 'contact_person',
                'contact_no', 'website', 'google_map', 'description', 'image', 'image_tag'
            )
        }),
        ('📋 Status & Assignment', {
            'fields': (
                'status', 'followup_meeting', 'find_form', 'googlemap_status', 'assigned_to'
            )
        }),
        ('🕓 Audit Info', {
            'fields': ('slug', 'created_by', 'updated_by', 'create_at', 'update_at')
        }),
    )

    inlines = [MeetingInline, FollowupInline, CommentInline, VoiceRecordingInline, VisitInline]

    tab_fieldsets = (
        ('🏢 Company Information', 'Company Information'),
        ('📋 Status & Assignment', 'Status & Assignment'),
        ('🕓 Audit Info', 'Audit Info'),
    )

    tab_inlines = [
        ('🗓 Meetings', MeetingInline),
        ('🔁 Followups', FollowupInline),
        ('💬 Comments', CommentInline),
        ('🎤 Voice Recordings', VoiceRecordingInline),
        ('👣 Visits', VisitInline),
    ]

    tab_icons = {
        '🏢 Company Information': 'fas fa-building',
        '📋 Status & Assignment': 'fas fa-tasks',
        '🕓 Audit Info': 'fas fa-clock',
        '🗓 Meetings': 'fas fa-calendar-check',
        '🔁 Followups': 'fas fa-sync',
        '💬 Comments': 'fas fa-comments',
        '🎤 Voice Recordings': 'fas fa-microphone',
        '👣 Visits': 'fas fa-walking'
    }

    list_per_page = 20
# ============================================================
# Sub Admins
# ============================================================
@admin.register(Meeting)
class MeetingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'company', 'company_contact', 'status', 'meeting_date', 'assigned_to', 'create_at')
    list_filter = ('status', 'assigned_to')
    search_fields = ('company__company_name', 'comment')
    readonly_fields = ('create_at', 'update_at', 'created_by', 'updated_by')

    def company_contact(self, obj):
        return obj.company.contact_no if obj.company else None
    company_contact.short_description = "Contact No"
    list_per_page = 20



@admin.register(Followup)
class FollowupAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'company', 'company_contact', 'status', 'followup_date', 'assigned_to', 'create_at')
    list_filter = ('status', 'assigned_to')
    search_fields = ('company__company_name', 'comment')
    readonly_fields = ('create_at', 'update_at', 'created_by', 'updated_by')

    def company_contact(self, obj):
        return obj.company.contact_no if obj.company else None
    company_contact.short_description = "Contact No"

    list_per_page = 20


@admin.register(Comment)
class CommentAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'company', 'company_contact', 'comment', 'created_by', 'create_at')
    search_fields = ('company__company_name', 'comment')
    readonly_fields = ('create_at', 'update_at', 'created_by', 'updated_by')

    def company_contact(self, obj):
        return obj.company.contact_no if obj.company else None
    company_contact.short_description = "Contact No"

    list_per_page = 20



@admin.register(VoiceRecording)
class VoiceRecordingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'company', 'company_contact', 'file', 'uploaded_by', 'uploaded_at')
    search_fields = ('company__company_name',)
    readonly_fields = ('uploaded_by', 'uploaded_at')

    def company_contact(self, obj):
        return obj.company.contact_no if obj.company else None
    company_contact.short_description = "Contact No"


@admin.register(Visit)
class VisitAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'company', 'company_contact', 'visit_type', 'visit_status', 'uploaded_by', 'uploaded_at')
    list_filter = ('visit_type', 'visit_status')
    search_fields = ('company__company_name',)
    readonly_fields = ('uploaded_by', 'uploaded_at')

    def company_contact(self, obj):
        return obj.company.contact_no if obj.company else None
    company_contact.short_description = "Contact No"


# ============================================================
# Minor Models
# ============================================================
@admin.register(Approx)
class ApproxAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'city', 'locality', 'create_at')
    search_fields = ('title',)
    list_filter = ('category', 'city', 'locality')


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'socia_site', 'link')
    search_fields = ('link', 'company__company_name')
    list_filter = ('socia_site',)
    autocomplete_fields = ('company',)


@admin.register(Error)
class ErrorAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'title', 'error')
    search_fields = ('title', 'error', 'company__company_name')
    autocomplete_fields = ('company',)


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'title', 'image')
    search_fields = ('title', 'product__company_name')
    autocomplete_fields = ('product',)


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'questions')
    search_fields = ('questions', 'company__company_name')
    autocomplete_fields = ('company',)

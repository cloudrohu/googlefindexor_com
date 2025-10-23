from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
import admin_thumbnails

from .models import (
    Company, Comment, VoiceRecording, Approx,
    SocialLink, Error, Images, Faq, Visit,
    Meeting, Followup
)

# ======================================================
# COMPANY INFO MIXIN (for inline models)
# ======================================================
class CompanyInfoMixin:
    """Display Company main details inside inlines."""

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


# ======================================================
# INLINE MODELS (Company fields visible)
# ======================================================
class CommentInline(CompanyInfoMixin, admin.TabularInline):
    model = Comment
    extra = 1
    fields = ('company_name', 'company_city', 'company_locality', 'company_contact', 'comment', 'create_at', 'update_at')
    readonly_fields = ('company_name', 'company_city', 'company_locality', 'company_contact', 'create_at', 'update_at')
    show_change_link = True


class VoiceRecordingInline(CompanyInfoMixin, admin.TabularInline):
    model = VoiceRecording
    extra = 1
    fields = ('company_name', 'company_city', 'company_locality', 'company_contact', 'file', 'uploaded_at')
    readonly_fields = ('company_name', 'company_city', 'company_locality', 'company_contact', 'uploaded_at')
    show_change_link = True


class VisitInline(CompanyInfoMixin, admin.TabularInline):
    model = Visit
    extra = 1
    fields = ('company_name', 'company_city', 'company_locality', 'company_contact', 'visit_type', 'visit_for', 'visit_status', 'comment', 'uploaded_by', 'uploaded_at')
    readonly_fields = ('company_name', 'company_city', 'company_locality', 'company_contact', 'uploaded_at')
    show_change_link = True


class MeetingInline(CompanyInfoMixin, admin.TabularInline):
    model = Meeting
    extra = 1
    fields = ('company_name', 'company_city', 'company_locality', 'company_contact', 'status', 'meeting_date', 'assigned_to', 'comment', 'create_at', 'update_at')
    readonly_fields = ('company_name', 'company_city', 'company_locality', 'company_contact', 'create_at', 'update_at')
    show_change_link = True


class FollowupInline(CompanyInfoMixin, admin.TabularInline):
    model = Followup
    extra = 1
    fields = ('company_name', 'company_city', 'company_locality', 'company_contact', 'status', 'followup_date', 'assigned_to', 'comment', 'create_at', 'update_at')
    readonly_fields = ('company_name', 'company_city', 'company_locality', 'company_contact', 'create_at', 'update_at')
    show_change_link = True


# ======================================================
# COMPANY ADMIN
# ======================================================
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    
    list_display = (
        "id", "company_name", "category", "city", "locality", 'followup_meeting',
        "contact_person", "contact_no", 'address', 'website', 'google_map',
        'description', "image_tag", "create_at", 'created_by', 'updated_by', 'update_at', "assigned_to"
    )

    list_filter = (
        "status",
        ("followup_meeting", admin.DateFieldListFilter),
        "find_form",
        "googlemap_status",
        ("created_by", admin.RelatedOnlyFieldListFilter),
        ("assigned_to", admin.RelatedOnlyFieldListFilter),
        ("category", admin.RelatedOnlyFieldListFilter),
        ("city", admin.RelatedOnlyFieldListFilter),
        ("locality", admin.RelatedOnlyFieldListFilter),
        ("create_at", admin.DateFieldListFilter),
    )

    search_fields = ("company_name", "contact_person", "contact_no", "city__name", "locality__name")
    readonly_fields = ("slug", "create_at", "update_at", "image_tag", "created_by_display", "updated_by_display")

    inlines = [MeetingInline, FollowupInline, CommentInline, VoiceRecordingInline, VisitInline]
    ordering = ["-create_at"]

    fieldsets = (
        ("Basic Details", {
            "fields": (
                "company_name", "category", "city", "locality", "address",
                "contact_person", "contact_no", "website", "google_map", "description", "image", "image_tag"
            )
        }),
        ("Follow Up & Status", {
            "fields": (
                "status", "followup_meeting", "find_form", "googlemap_status", "assigned_to"
            )
        }),
        ("Meta Info", {
            "fields": ("slug", "create_at", "update_at", "created_by_display", "updated_by_display")
        }),
    )

    # Auto set user fields
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            if hasattr(obj, 'created_by') and not obj.created_by:
                obj.created_by = request.user
            if hasattr(obj, 'updated_by'):
                obj.updated_by = request.user
            if hasattr(obj, 'uploaded_by') and not obj.uploaded_by:
                obj.uploaded_by = request.user
            obj.save()
        formset.save_m2m()

    def created_by_display(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name() or obj.created_by.username
        return "-"
    created_by_display.short_description = "Created by"

    def updated_by_display(self, obj):
        if obj.updated_by:
            return obj.updated_by.get_full_name() or obj.updated_by.username
        return "-"
    updated_by_display.short_description = "Updated by"


# ======================================================
# OTHER ADMINS (No change needed)
# ======================================================
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "short_comment", "created_by", "create_at")
    search_fields = ("company__company_name", "comment")
    list_filter = ("create_at",)
    ordering = ["-create_at"]

    def short_comment(self, obj):
        return (obj.comment[:50] + '...') if obj.comment and len(obj.comment) > 50 else obj.comment
    short_comment.short_description = "Comment"


@admin.register(VoiceRecording)
class VoiceRecordingAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "file", "uploaded_by", "uploaded_at")
    list_filter = ("uploaded_at",)
    search_fields = ("company__company_name",)
    ordering = ["-uploaded_at"]


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "visit_type", "visit_for", "visit_status", "uploaded_by", "uploaded_at")
    list_filter = ("visit_type", "visit_status", "uploaded_at")
    search_fields = ("company__company_name", "comment")
    ordering = ["-uploaded_at"]


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "status", "meeting_date", "assigned_to", "created_by", "create_at")
    list_filter = ("status", "assigned_to", "create_at")
    search_fields = ("company__company_name", "comment")
    ordering = ["-create_at"]


@admin.register(Followup)
class FollowupAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "status", "followup_date", "assigned_to", "created_by", "create_at")
    list_filter = ("status", "assigned_to", "create_at")
    search_fields = ("company__company_name", "comment")
    ordering = ["-create_at"]


@admin.register(Approx)
class ApproxAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "city", "locality", "create_at")
    search_fields = ("title",)
    list_filter = ("category", "city", "locality")
    list_per_page = 30


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "socia_site", "link")
    search_fields = ("link", "company__company_name")
    list_filter = ("socia_site",)
    list_per_page = 30
    autocomplete_fields = ("company",)


@admin.register(Error)
class ErrorAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "title", "error")
    search_fields = ("title", "error", "company__company_name")
    list_per_page = 30
    autocomplete_fields = ("company",)


@admin_thumbnails.thumbnail("image")
@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "title", "image_thumbnail")
    search_fields = ("title", "product__company_name")
    list_per_page = 30
    autocomplete_fields = ("product",)


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "questions")
    search_fields = ("questions", "company__company_name")
    list_per_page = 30
    autocomplete_fields = ("company",)

from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
import admin_thumbnails

from .models import (
    Company, Comment, VoiceRecording, Approx,
    SocialLink, Error, Images, Faq, Visit,
    Meeting, Followup  # ✅ added new models
)

# ==========================
# INLINE FOR COMMENTS
# ==========================
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ('comment', 'create_at', 'update_at')
    readonly_fields = ('create_at', 'update_at')
    show_change_link = True


# ==========================
# INLINE FOR VOICE RECORDINGS
# ==========================
class VoiceRecordingInline(admin.TabularInline):
    model = VoiceRecording
    extra = 1
    fields = ('file', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
    show_change_link = True


# ==========================
# INLINE FOR VISITS
# ==========================
class VisitInline(admin.TabularInline):
    model = Visit
    extra = 1
    fields = ('visit_type', 'visit_for', 'visit_status', 'comment', 'uploaded_by', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
    show_change_link = True


# ==========================
# INLINE FOR MEETINGS
# ==========================
class MeetingInline(admin.TabularInline):
    model = Meeting
    extra = 1
    fields = ('status', 'meeting_date', 'assigned_to', 'comment', 'create_at', 'update_at')
    readonly_fields = ('create_at', 'update_at')
    show_change_link = True


# ==========================
# INLINE FOR FOLLOWUPS
# ==========================
class FollowupInline(admin.TabularInline):
    model = Followup
    extra = 1
    fields = ('status', 'followup_date', 'assigned_to', 'comment', 'create_at', 'update_at')
    readonly_fields = ('create_at', 'update_at')
    show_change_link = True


# ======================================================
# COMPANY ADMIN
# ======================================================
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "id", "company_name", "category", "city", "locality",
        "contact_person", "contact_no", "image_tag", "create_at", "assigned_to"
    )

    # ✅ Correct, complete, and optimized filters
    list_filter = (
        "status",                     # choice field ✅
        ("followup_meeting", admin.DateFieldListFilter),  # datetime field ✅
        "find_form",                  # foreign key ✅
        "googlemap_status",           # foreign key ✅
        ("created_by", admin.RelatedOnlyFieldListFilter), # foreign key (user)
        ("assigned_to", admin.RelatedOnlyFieldListFilter),# staff FK
        ("category", admin.RelatedOnlyFieldListFilter),   # category FK
        ("city", admin.RelatedOnlyFieldListFilter),       # city FK
        ("locality", admin.RelatedOnlyFieldListFilter),   # locality FK
        ("create_at", admin.DateFieldListFilter),         # datetime ✅
    )

    search_fields = ("company_name", "contact_person", "contact_no", "city__name", "locality__name")
    readonly_fields = (
        "slug", "create_at", "update_at", "image_tag",
        "created_by_display", "updated_by_display"
    )
    # ✅ added new inlines here
    inlines = [
        MeetingInline,
        FollowupInline,
        CommentInline,
        VoiceRecordingInline,
        VisitInline,
    ]
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
                "status", "followup_meeting",
                "find_form", "googlemap_status", "assigned_to"
            )
        }),
        ("Meta Info", {
            "fields": (
                "slug", "create_at", "update_at",
                "created_by_display", "updated_by_display"
            )
        }),
    )

    # ✅ Auto-set created_by and updated_by
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    # ✅ Auto-fill for inlines (Meeting, Followup, etc.)
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

    # ✅ Custom readonly display fields
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
# COMMENT ADMIN
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


# ======================================================
# VOICE RECORDING ADMIN
# ======================================================
@admin.register(VoiceRecording)
class VoiceRecordingAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "file", "uploaded_by", "uploaded_at")
    list_filter = ("uploaded_at",)
    search_fields = ("company__company_name",)
    ordering = ["-uploaded_at"]


# ======================================================
# VISIT ADMIN
# ======================================================
@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "visit_type", "visit_for", "visit_status", "uploaded_by", "uploaded_at")
    list_filter = ("visit_type", "visit_status", "uploaded_at")
    search_fields = ("company__company_name", "comment")
    ordering = ["-uploaded_at"]


# ======================================================
# MEETING ADMIN
# ======================================================
@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "status", "meeting_date", "assigned_to", "created_by", "create_at")
    list_filter = ("status", "assigned_to", "create_at")
    search_fields = ("company__company_name", "comment")
    ordering = ["-create_at"]


# ======================================================
# FOLLOWUP ADMIN
# ======================================================
@admin.register(Followup)
class FollowupAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "status", "followup_date", "assigned_to", "created_by", "create_at")
    list_filter = ("status", "assigned_to", "create_at")
    search_fields = ("company__company_name", "comment")
    ordering = ["-create_at"]


# ======================================================
# OTHER ADMINS (same as before)
# ======================================================
class ApproxAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "city", "locality", "create_at")
    search_fields = ("title",)
    list_filter = ("category", "city", "locality")
    list_per_page = 30


class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "socia_site", "link")
    search_fields = ("link", "company__company_name")
    list_filter = ("socia_site",)
    list_per_page = 30
    autocomplete_fields = ("company",)


class ErrorAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "title", "error")
    search_fields = ("title", "error", "company__company_name")
    list_per_page = 30
    autocomplete_fields = ("company",)


@admin_thumbnails.thumbnail("image")
class ImagesAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "title", "image_thumbnail")
    search_fields = ("title", "product__company_name")
    list_per_page = 30
    autocomplete_fields = ("product",)


class FaqAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "questions")
    search_fields = ("questions", "company__company_name")
    list_per_page = 30
    autocomplete_fields = ("company",)


# ======================================================
# REGISTER ALL MODELS
# ======================================================
admin.site.register(Approx, ApproxAdmin)
admin.site.register(SocialLink, SocialLinkAdmin)
admin.site.register(Error, ErrorAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Faq, FaqAdmin)

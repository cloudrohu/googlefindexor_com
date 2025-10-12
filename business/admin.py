from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
import admin_thumbnails

from .models import (
    Company, Comment, VoiceRecording, Approx,
    SocialLink, Error, Follow_Up, Images, Faq,
    Meeting, Visit
)

# ==========================
# INLINE FOR COMMENTS
# ==========================
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ('comment', 'created_by', 'updated_by', 'create_at', 'update_at')
    readonly_fields = ('create_at', 'update_at')
    show_change_link = True


# ==========================
# INLINE FOR VOICE RECORDINGS
# ==========================
class VoiceRecordingInline(admin.TabularInline):
    model = VoiceRecording
    extra = 1
    fields = ('file', 'note', 'uploaded_by', 'uploaded_at')
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
# COMPANY ADMIN
# ==========================
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "id", "company_name", "category", "city", "locality",
        "contact_person", "contact_no", "image_tag", "create_at", "assigned_to"
    )
    list_filter = ("category", "city", "locality", "create_at", "assigned_to")
    search_fields = ("company_name", "contact_person", "contact_no", "city__name", "locality__name")
    readonly_fields = ("slug", "create_at", "update_at", "image_tag")
    # ❌ remove this line:
    # prepopulated_fields = {"slug": ("company_name",)}
    inlines = [CommentInline, VoiceRecordingInline, VisitInline]
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
                "call_status", "call_comment", "followup_meeting",
                "find_form", "googlemap_status", "assigned_to"
            )
        }),
        ("Meta Info", {
            "fields": ("slug", "create_at", "update_at", "created_by", "updated_by")
        }),
    )

# ==========================
# COMMENT ADMIN
# ==========================
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "short_comment", "created_by", "create_at")
    search_fields = ("company__company_name", "comment")
    list_filter = ("create_at",)
    ordering = ["-create_at"]

    def short_comment(self, obj):
        return (obj.comment[:50] + '...') if obj.comment and len(obj.comment) > 50 else obj.comment
    short_comment.short_description = "Comment"


# ==========================
# VOICE RECORDING ADMIN
# ==========================
@admin.register(VoiceRecording)
class VoiceRecordingAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "file", "note", "uploaded_by", "uploaded_at")
    list_filter = ("uploaded_at",)
    search_fields = ("company__company_name", "note")
    ordering = ["-uploaded_at"]


# ==========================
# VISIT ADMIN
# ==========================
@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "visit_type", "visit_for", "visit_status", "uploaded_by", "uploaded_at")
    list_filter = ("visit_type", "visit_status", "uploaded_at")
    search_fields = ("company__company_name", "comment")
    ordering = ["-uploaded_at"]


# ======================================================
# APPROX ADMIN
# ======================================================
class ApproxAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "city", "locality", "create_at")
    search_fields = ("title",)
    list_filter = ("category", "city", "locality")
    list_per_page = 30


# ======================================================
# SOCIAL LINK ADMIN
# ======================================================
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "socia_site", "link")
    search_fields = ("link", "company__company_name")
    list_filter = ("socia_site",)
    list_per_page = 30
    autocomplete_fields = ("company",)


# ======================================================
# ERROR ADMIN
# ======================================================
class ErrorAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "title", "error")
    search_fields = ("title", "error", "company__company_name")
    list_per_page = 30
    autocomplete_fields = ("company",)


# ======================================================
# FOLLOW UP ADMIN
# ======================================================
class FollowUpAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "follow_up", "comment")
    list_filter = ("follow_up",)
    search_fields = ("comment", "company__company_name")
    autocomplete_fields = ("company",)
    list_per_page = 30


# ======================================================
# IMAGES ADMIN
# ======================================================
@admin_thumbnails.thumbnail("image")
class ImagesAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "title", "image_thumbnail")
    search_fields = ("title", "product__company_name")
    list_per_page = 30
    autocomplete_fields = ("product",)


# ======================================================
# FAQ ADMIN
# ======================================================
class FaqAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "questions")
    search_fields = ("questions", "company__company_name")
    list_per_page = 30
    autocomplete_fields = ("company",)


# ======================================================
# MEETING ADMIN
# ======================================================
class MeetingAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "meeting", "comment")
    list_filter = ("meeting",)
    search_fields = ("comment", "company__company_name")
    autocomplete_fields = ("company",)
    list_per_page = 30


# ======================================================
# REGISTER ALL MODELS
# ======================================================
admin.site.register(Approx, ApproxAdmin)
admin.site.register(SocialLink, SocialLinkAdmin)
admin.site.register(Error, ErrorAdmin)
admin.site.register(Follow_Up, FollowUpAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Faq, FaqAdmin)
admin.site.register(Meeting, MeetingAdmin)

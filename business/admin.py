from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
import admin_thumbnails

from .models import (
    Company, Comment, VoiceRecording, Approx,
    SocialLink, Error, Follow_Up, Images, Faq,
    Meeting, Visit
)


# ======================================================
# COMPANY ADMIN
# ======================================================
@admin_thumbnails.thumbnail("image")
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "id", "image_thumbnail", "company_name",
        "category", "city", "locality",
        "call_status", "googlemap_status",
        "assigned_to", "create_at"
    )
    list_filter = (
        "category", "city", "locality",
        "call_status", "googlemap_status", "assigned_to"
    )
    search_fields = (
        "company_name", "contact_person",
        "contact_no", "website", "address"
    )
    list_per_page = 25
    readonly_fields = ("slug", "image_tag")
    fieldsets = (
        ("Company Information", {
            "fields": (
                "category", "company_name", "contact_person", "contact_no",
                "city", "locality", "address", "website", "google_map",
                "description", "image", "image_tag"
            )
        }),
        ("Status & Assignment", {
            "fields": ("call_status", "call_comment", "googlemap_status", "find_form", "assigned_to")
        }),
        ("System Fields", {
            "fields": ("slug",)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


# ======================================================
# COMMENT ADMIN
# ======================================================
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "comment", "created_by", "create_at")
    search_fields = ("comment", "company__company_name")
    list_filter = ("create_at", "created_by")
    autocomplete_fields = ("company",)
    list_per_page = 30


# ======================================================
# VOICE RECORDING ADMIN
# ======================================================
class VoiceRecordingAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "file", "uploaded_by", "uploaded_at")
    search_fields = ("company__company_name", "note")
    list_filter = ("uploaded_at", "uploaded_by")
    autocomplete_fields = ("company",)
    list_per_page = 30


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
# VISIT ADMIN
# ======================================================
class VisitAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "comment", "visit_date")
    list_filter = ("visit_date",)
    search_fields = ("comment", "company__company_name")
    autocomplete_fields = ("company",)
    list_per_page = 30


# ======================================================
# REGISTER ALL MODELS
# ======================================================
admin.site.register(Company, CompanyAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(VoiceRecording, VoiceRecordingAdmin)
admin.site.register(Approx, ApproxAdmin)
admin.site.register(SocialLink, SocialLinkAdmin)
admin.site.register(Error, ErrorAdmin)
admin.site.register(Follow_Up, FollowUpAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Faq, FaqAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Visit, VisitAdmin)

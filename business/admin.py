import admin_thumbnails
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from mptt.admin import DraggableMPTTAdmin

from .models import Category, Company, Approx, SocialLink, Error, Follow_Up, Images, Faq, Meeting, Visit


# ===================== Resources =====================
class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ("id", "title", "keywords", "description", "status", "slug", "parent")


class CompanyResource(resources.ModelResource):
    class Meta:
        model = Company
        fields = (
            "id",
            "company_name",
            "category",
            "contact_person",
            "contact_no",
            "email",
            "city",
            "locality",
            "sub_locality",
            "address",
            "keywords",
            "website",
            "google_map",
            "description",
            "about",
            "call_status",
            "call_comment",
            "followup_meeting",
            "find_form",
            "googlemap_status",
            "slug",
            "created_by",
            "updated_by",
        )


class ApproxResource(resources.ModelResource):
    class Meta:
        model = Approx
        fields = ("id", "title", "category", "city", "locality")


class SocialLinkResource(resources.ModelResource):
    class Meta:
        model = SocialLink
        fields = ("id", "company", "socia_site", "link")


class ErrorResource(resources.ModelResource):
    class Meta:
        model = Error
        fields = ("id", "company", "title", "error")


class FollowUpResource(resources.ModelResource):
    class Meta:
        model = Follow_Up
        fields = ("id", "company", "follow_up", "comment")


class ImagesResource(resources.ModelResource):
    class Meta:
        model = Images
        fields = ("id", "product", "title", "image")


class FaqResource(resources.ModelResource):
    class Meta:
        model = Faq
        fields = ("id", "company", "questions", "answers")


class MeetingResource(resources.ModelResource):
    class Meta:
        model = Meeting
        fields = ("id", "company", "meeting", "comment")


class VisitResource(resources.ModelResource):
    class Meta:
        model = Visit
        fields = ("id", "company", "comment", "visit_date")


# ===================== Admins =====================

class CategoryAdmin(ImportExportModelAdmin, DraggableMPTTAdmin):
    resource_class = CategoryResource
    mptt_indent_field = "title"
    list_display = ("id", "tree_actions", "indented_title", "slug", "status")
    list_display_links = ("indented_title",)
    search_fields = ("title", "keywords")
    list_per_page = 30
    prepopulated_fields = {"slug": ("title",)}


@admin_thumbnails.thumbnail("image")
class CompanyAdmin(ImportExportModelAdmin):
    resource_class = CompanyResource
    list_display = (
        "id",
        "image_thumbnail",
        "company_name",
        "category",
        "contact_person",
        "contact_no",
        "email",
        "city",
        "locality",
        "sub_locality",
        "address",
        "website",
        "googlemap_status",
        "call_status",
        "followup_meeting",
    )
    list_filter = ("city", "locality", "sub_locality", "category", "call_status", "googlemap_status")
    search_fields = ("company_name", "contact_person", "contact_no", "email", "website")
    list_per_page = 20


class ApproxAdmin(ImportExportModelAdmin):
    resource_class = ApproxResource
    list_display = ("id", "title", "category", "city", "locality")
    list_filter = ("category", "city", "locality")
    search_fields = ("title",)
    list_per_page = 30


class SocialLinkAdmin(ImportExportModelAdmin):
    resource_class = SocialLinkResource
    list_display = ("id", "company", "socia_site", "link")
    list_filter = ("socia_site",)
    search_fields = ("link",)
    list_per_page = 30


class ErrorAdmin(ImportExportModelAdmin):
    resource_class = ErrorResource
    list_display = ("id", "company", "title", "error")
    search_fields = ("title", "error")
    list_per_page = 30


class FollowUpAdmin(ImportExportModelAdmin):
    resource_class = FollowUpResource
    list_display = ("id", "company", "follow_up", "comment")
    list_filter = ("follow_up",)
    search_fields = ("comment", "company__company_name")
    list_per_page = 30


class ImagesAdmin(ImportExportModelAdmin):
    resource_class = ImagesResource
    list_display = ("id", "product", "title", "image")
    search_fields = ("title",)
    list_per_page = 30


class FaqAdmin(ImportExportModelAdmin):
    resource_class = FaqResource
    list_display = ("id", "company", "questions", "answers")
    search_fields = ("questions",)
    list_per_page = 30


class MeetingAdmin(ImportExportModelAdmin):
    resource_class = MeetingResource
    list_display = ("id", "company", "meeting", "comment")
    list_filter = ("meeting",)
    search_fields = ("comment",)
    list_per_page = 30


class VisitAdmin(ImportExportModelAdmin):
    resource_class = VisitResource
    list_display = ("id", "company", "comment", "visit_date")
    list_filter = ("visit_date",)
    search_fields = ("comment", "company__company_name")
    list_per_page = 30


# ===================== Register =====================

admin.site.register(Category, CategoryAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Approx, ApproxAdmin)
admin.site.register(SocialLink, SocialLinkAdmin)
admin.site.register(Error, ErrorAdmin)
admin.site.register(Follow_Up, FollowUpAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Faq, FaqAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Visit, VisitAdmin)

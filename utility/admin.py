import admin_thumbnails
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from mptt.admin import DraggableMPTTAdmin

from .models import (
    City, Locality, Sub_Locality,
    Find_Form, Call_Status, SocialSite,
    Googlemap_Status, Response_Status, RequirementType
)

# ------------------------------
# Resources for Import/Export
# ------------------------------

class LocalityResource(resources.ModelResource):
    class Meta:
        model = Locality
        fields = ("id", "title", "parent", "slug")  # sirf actual fields
        import_id_fields = ("id",)  # id ke basis par update bhi ho sakta hai

class SubLocalityResource(resources.ModelResource):
    class Meta:
        model = Sub_Locality
        fields = "__all__"

class FindFormResource(resources.ModelResource):
    class Meta:
        model = Find_Form
        fields = "__all__"

class CallStatusResource(resources.ModelResource):
    class Meta:
        model = Call_Status
        fields = "__all__"

class SocialSiteResource(resources.ModelResource):
    class Meta:
        model = SocialSite
        fields = "__all__"

class GooglemapStatusResource(resources.ModelResource):
    class Meta:
        model = Googlemap_Status
        fields = "__all__"

class ResponseStatusResource(resources.ModelResource):
    class Meta:
        model = Response_Status
        fields = "__all__"

class RequirementTypeResource(resources.ModelResource):
    class Meta:
        model = RequirementType
        fields = "__all__"


# ------------------------------
# Admin Classes
# ------------------------------
# Resource
class CityResource(resources.ModelResource):
    class Meta:
        model = City
        fields = ("id", "title")   # sirf id aur title
        import_id_fields = ("id",) # id optional hai import ke time


# Admin
@admin.register(City)
class CityAdmin(ImportExportModelAdmin):
    resource_class = CityResource
    list_display = ("id", "title")
    search_fields = ("title",)

@admin.register(Locality)
class LocalityAdmin(ImportExportModelAdmin, DraggableMPTTAdmin):
    resource_class = LocalityResource
    mptt_indent_field = "title"
    list_display = ("id", "tree_actions", "indented_title", "slug")
    list_display_links = ("indented_title",)
    list_per_page = 30
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Sub_Locality)
class SubLocalityAdmin(ImportExportModelAdmin):
    resource_class = SubLocalityResource
    list_display = ("id", "__str__")
    search_fields = ("id",)

@admin.register(Find_Form)
class FindFormAdmin(ImportExportModelAdmin):
    resource_class = FindFormResource
    list_display = ("id", "__str__")

@admin.register(Call_Status)
class CallStatusAdmin(ImportExportModelAdmin):
    resource_class = CallStatusResource
    list_display = ("id", "__str__")

@admin.register(SocialSite)
class SocialSiteAdmin(ImportExportModelAdmin):
    resource_class = SocialSiteResource
    list_display = ("id", "__str__")

@admin.register(Googlemap_Status)
class GooglemapStatusAdmin(ImportExportModelAdmin):
    resource_class = GooglemapStatusResource
    list_display = ("id", "__str__")

@admin.register(Response_Status)
class ResponseStatusAdmin(ImportExportModelAdmin):
    resource_class = ResponseStatusResource
    list_display = ("id", "__str__")

@admin.register(RequirementType)
class RequirementTypeAdmin(ImportExportModelAdmin):
    resource_class = RequirementTypeResource
    list_display = ("id", "__str__")

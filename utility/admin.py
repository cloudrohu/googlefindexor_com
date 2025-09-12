
import admin_thumbnails
from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from .models import *

admin.site.register(City,)

class LocalityAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('id','tree_actions', 'indented_title', 'slug',
                    )
    list_display_links = ('indented_title',)
    
    list_per_page = 30 
    prepopulated_fields = {'slug': ('title',)}    


admin.site.register(Locality,LocalityAdmin)
admin.site.register(Sub_Locality,)


admin.site.register(Find_Form,)
admin.site.register(Call_Status,)
admin.site.register(SocialSite,)
admin.site.register(Googlemap_Status,)
admin.site.register(Response_Status,)
admin.site.register(RequirementType,)
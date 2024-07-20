import admin_thumbnails
from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from .models import *



class Follow_UpInline(admin.TabularInline):
    model = Follow_Up
    extra = 1
    show_change_link = True

class MeetingInline(admin.TabularInline):
    model = Meeting
    extra = 1
    show_change_link = True


class ResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'response_status','name','email_id','contact_no', 'description', 'call_comment','create_at','update_at','response_from',]    
    
    list_filter = ['create_at','response_status','response_from',]
    search_fields = ['name','email_id','contact_no', 'description',]
    list_editable = ['response_status',]
    list_per_page = 5
    inlines = [Follow_UpInline,MeetingInline]

class MeetingAdmin(admin.ModelAdmin):
    list_display = ['id', 'meeting','comment', 'name','create_at','update_at']    
    
    list_filter = ('meeting','create_at','update_at',) 
    list_per_page = 5


class Follow_UpAdmin(admin.ModelAdmin):
    list_display = ['id',  'follow_up','comment','name', 'create_at','update_at']    
    
    list_filter = ('follow_up','create_at','update_at',) 
    list_per_page = 5 




admin.site.register(Follow_Up,Follow_UpAdmin)
admin.site.register(Meeting,MeetingAdmin)
admin.site.register(Response,ResponseAdmin)
admin.site.register(Response_From,)
admin.site.register(Response_Status,)









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
    list_display = ['id','name','contact_no', 'call_comment','response_status','description','meeting_follow_up','locality_city','email_id','response_from',]    
    
    list_filter = ['meeting_follow_up','response_status','response_from','locality_city']
    search_fields = ['id','name','email_id','contact_no', 'description',]
    list_per_page = 20
    inlines = [Follow_UpInline,MeetingInline]

class MeetingAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','meeting','comment','locality_city','create_at','update_at',]    
    
    list_filter = ('meeting','create_at','update_at','locality_city',) 

    list_per_page = 20


class Follow_UpAdmin(admin.ModelAdmin):
    list_display = ['id','name','follow_up','comment','locality_city', 'create_at','update_at']    
    
    list_filter = ('follow_up','create_at','update_at','locality_city',) 

    list_per_page = 20 




admin.site.register(Follow_Up,Follow_UpAdmin)
admin.site.register(Meeting,MeetingAdmin)
admin.site.register(Response,ResponseAdmin)
admin.site.register(Response_From,)
admin.site.register(Response_Status,)









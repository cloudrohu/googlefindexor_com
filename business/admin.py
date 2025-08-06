import admin_thumbnails
from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from .models import *

  
class CategoryApproxInline(admin.TabularInline):
    model = Approx
    extra = 1
    show_change_link = True

class CompanySocialInline(admin.TabularInline):
    model = SocialLink
    extra = 1
    show_change_link = True

class CompanyErrorInline(admin.TabularInline):
    model = Error
    extra = 1
    show_change_link = True

class Follow_UpInline(admin.TabularInline):
    model = Follow_Up
    extra = 1
    show_change_link = True

class MeetingInline(admin.TabularInline):
    model = Meeting
    extra = 1
    show_change_link = True

class VisitInline(admin.TabularInline):
    model = Visit
    extra = 1
    show_change_link = True


class ImagesInline(admin.TabularInline):
    model = Images
    extra = 1
    show_change_link = True


class FaqInline(admin.TabularInline):
    model = Faq
    extra = 1
    show_change_link = True


class ApproxAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'locality','city', 'title', ]
    list_filter = [ 'category', 'locality','city', ]

    search_fields = ['title']
    list_per_page = 30 

class SocialSiteAdmin(admin.ModelAdmin):
    list_display = ['id','title','code']
    search_fields = ['title']
    list_per_page = 30 

class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['id','company','link']
    search_fields = ['title']
    list_per_page = 30 

class ErrorAdmin(admin.ModelAdmin):
    list_display = ['id','title','error']
    search_fields = ['title']
    list_per_page = 30 


class FaqAdmin(admin.ModelAdmin):
    list_display = ['id','company','questions','answers']
    list_per_page = 30 

class imagesAdmin(admin.ModelAdmin):
    list_display = ['id']

    list_per_page = 30 

class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('id','tree_actions', 'indented_title', 'slug',
                    )
    list_display_links = ('indented_title',)
    
    list_per_page = 30 
    prepopulated_fields = {'slug': ('title',)}    
    inlines = [CategoryApproxInline,]


@admin_thumbnails.thumbnail('image')
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_thumbnail', 'find_form', 'call_status','call_comment', 'followup_meeting','company_name','category', 'contact_person','contact_no', 'description','email','website','address','sub_locality', 'locality','city','googlemap_status',]    
    
    list_filter = ('sub_locality','locality','city','category','followup_meeting','googlemap_status','call_status', 'find_form',) 
    search_fields = ['id','company_name','contact_person','contact_no', 'description','email','website',]
    list_per_page = 10 
    inlines = [CompanySocialInline,CompanyErrorInline,Follow_UpInline,MeetingInline,VisitInline,ImagesInline,FaqInline]

@admin_thumbnails.thumbnail('image')
class MeetingAdmin(admin.ModelAdmin):
    list_display = ['id', 'meeting','comment', 'company','create_at','update_at']    
    
    list_filter = ('meeting','create_at','update_at',) 
    list_per_page = 30 


@admin_thumbnails.thumbnail('image')
class Follow_UpAdmin(admin.ModelAdmin):
    list_display = ['id',  'follow_up','comment','company', 'create_at','update_at']    
    
    list_filter = ('follow_up','create_at','update_at',) 
    list_per_page = 30 


admin.site.register(SocialLink,SocialLinkAdmin)
admin.site.register(Approx,ApproxAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Company,CompanyAdmin)

admin.site.register(Follow_Up,Follow_UpAdmin)
admin.site.register(Meeting,MeetingAdmin)
admin.site.register(Visit)
admin.site.register(Faq,FaqAdmin)
admin.site.register(Images,imagesAdmin)








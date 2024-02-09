from django.contrib import admin
import admin_thumbnails

from .models import *
# Register your models here.

class SettingtAdmin(admin.ModelAdmin):
    list_display = ['title','company', 'update_at','status']

@admin_thumbnails.thumbnail('image')
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title','image_tag','featured_project', 'create_at','update_at']

@admin_thumbnails.thumbnail('image')
class OfferAdmin(admin.ModelAdmin):
    list_display = ['title','image_tag', 'update_at','create_at']


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name','subject', 'update_at','status','note','message','email','ip',]
    list_editable = ['status','note']
    readonly_fields =('name','subject','email','message','ip')
    list_filter = ['status']

admin.site.register(Setting,SettingtAdmin)

admin.site.register(ContactMessage,ContactMessageAdmin)
admin.site.register(Offer,OfferAdmin)
admin.site.register(Slider,SliderAdmin)
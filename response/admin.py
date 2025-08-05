from django.contrib import admin
from .models import Response, Meeting_Follow_Up

class Meeting_Follow_UpInline(admin.TabularInline):
    model = Meeting_Follow_Up
    extra = 1
    show_change_link = True

    exclude = ['created_by', 'updated_by']


class ResponseAdmin(admin.ModelAdmin):
    list_display = ['id','call_status','contact_no','description', 'update_at','create_at','created_by','updated_by']    
    list_filter = ['call_status']
    search_fields = ['id','contact_no', 'description']
    list_per_page = 10
    inlines = [Meeting_Follow_UpInline]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


    exclude = ['created_by', 'updated_by']

    # Auto fill user
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # New object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class Meeting_Follow_UpAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'type','Meeting_follow_up','contact_porsone','locality_city', 
        'business_name', 'business_category', 'response_status', 
        'city', 'email_id','create_at','update_at', 'created_by', 'updated_by'
    ]    
    list_filter = (
        'type','Meeting_follow_up','locality_city',
        'business_category','response_status','city',
        'create_at','update_at'
    )
    list_per_page = 10


    # Auto fill user
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # New object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Meeting_Follow_Up, Meeting_Follow_UpAdmin)
admin.site.register(Response, ResponseAdmin)

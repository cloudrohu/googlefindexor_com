from django.contrib import admin
from .models import Response, Meeting_Follow_Up

class Meeting_Follow_UpInline(admin.TabularInline):
    model = Meeting_Follow_Up
    extra = 1
    show_change_link = True

    exclude = ['created_by', 'updated_by']


from django import forms
from .models import Response

class ResponseAdminForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = '__all__'

    def clean_contact_no(self):
        contact_no = self.cleaned_data.get('contact_no')
        if contact_no:
            contact_no = contact_no.replace(" ", "")
        return contact_no


class ResponseAdmin(admin.ModelAdmin):
    list_display = ['id','call_status','contact_no','comment', 'contact_persone', 'business_name', 'business_category', 'response_status', 'update_at','create_at','created_by','updated_by']    
    list_filter = ['call_status']
    list_editable = ['call_status']
    search_fields = ['id','contact_no', 'comment']
    list_per_page = 10
    inlines = [Meeting_Follow_UpInline]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    form = ResponseAdminForm


    exclude = ['created_by', 'updated_by']

    # Auto fill user
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # New object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class Meeting_Follow_UpAdmin(admin.ModelAdmin):
    list_display = [
        'id','response','Meeting_follow_up', 'description','locality_city', 
        'city','create_at','update_at', 'created_by', 'updated_by'
    ]    
    list_filter = (
        'Meeting_follow_up','locality_city',
        'city',
        'create_at','update_at'
    )
    list_editable = ['Meeting_follow_up','locality_city', 
        'city']
    list_per_page = 10


    # Auto fill user
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # New object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Meeting_Follow_Up, Meeting_Follow_UpAdmin)
admin.site.register(Response, ResponseAdmin)


from django.contrib import admin
from .models import Response, Meeting,Followup

class MeetingInline(admin.TabularInline):
    model = Meeting
    extra = 1
    show_change_link = True

    exclude = ['created_by', 'updated_by']

class FollowupInline(admin.TabularInline):
    model = Followup
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
    list_display = ['id','status','contact_no','comment', 'contact_persone', 'business_name','update_at','create_at','created_by','updated_by']    
    list_filter = ['status']
    list_editable = ['status']
    search_fields = ['id','contact_no', 'comment']
    list_per_page = 15
    inlines = [MeetingInline,FollowupInline]

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

class MeetingAdmin(admin.ModelAdmin):
    list_display = [
        'id','response','meeting', 'description','locality_city', 
        'city','create_at','update_at', 'created_by', 'updated_by'
    ]    
    list_filter = (
        'meeting','locality_city',
        'city',
        'create_at','update_at'
    )
    list_editable = ['meeting','locality_city', 
        'city']
    list_per_page = 15


    # Auto fill user
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # New object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)



class FollowupAdmin(admin.ModelAdmin):
    list_display = [
        'id','response','followup', 'description','locality_city', 
        'city','create_at','update_at', 'created_by', 'updated_by'
    ]    
    list_filter = (
        'followup','locality_city',
        'city',
        'create_at','update_at'
    )
    list_editable = ['followup','locality_city', 
        'city']
    list_per_page = 15


    # Auto fill user
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # New object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Followup, FollowupAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Response, ResponseAdmin)






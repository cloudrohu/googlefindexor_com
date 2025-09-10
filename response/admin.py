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
    list_display = [
        'get_mr_id',   # <-- yahan custom MR id show karenge
        'status',
        'contact_no',
        'comment',
        'contact_persone',
        'business_name',
        'business_category',
        'locality_city',
        'city',
        'update_at',
        'create_at',
        'created_by',
        'updated_by'
    ]    
    list_filter = ['status','locality_city','city','business_category',]
    list_editable = ['status','locality_city','city','business_category',]
    search_fields = ['id','contact_no', 'comment']
    list_per_page = 15
    inlines = [MeetingInline, FollowupInline]

    # Custom MR id
    def get_mr_id(self, obj):
        return f"MR{obj.id}"
    get_mr_id.short_description = "ID"   # column heading

class MeetingAdmin(admin.ModelAdmin):

    list_display = (
        "id", 
        "response", 
        "get_response_contact_no", 
        "meeting", 
        "get_response_comment",
        "get_response_business_name",
        "get_response_business_category",
        "get_response_locality",
        "get_response_city",
        "get_response_create_at",
        "get_response_update_at", 
        "get_response_created_by", 
        "get_response_updated_by"
    )
    list_filter = ("meeting","response__city", "response__locality_city","response__business_category",)
    search_fields = ("response__id", "response__business_name", "response__contact_no")
    list_editable = ["meeting"]
    list_per_page = 15

    def get_response_comment(self, obj):
        return obj.response.comment if obj.response else "-"
    get_response_comment.short_description = "Response Comment"

    def get_response_contact_no(self, obj):
        return obj.response.contact_no if obj.response else "-"
    get_response_contact_no.short_description = "Response Contact No"

    def get_response_city(self, obj):
        return obj.response.city if obj.response and obj.response.city else "-"
    get_response_city.short_description = "City"

    def get_response_locality(self, obj):
        return obj.response.locality_city if obj.response and obj.response.locality_city else "-"
    get_response_locality.short_description = "Locality"

    def get_response_business_name(self, obj):
        return obj.response.business_name if obj.response and obj.response.business_name else "-"
    get_response_business_name.short_description = "Business Name"

    def get_response_business_category(self, obj):
        return obj.response.business_category if obj.response and obj.response.business_category else "-"
    get_response_business_category.short_description = "Business Category"

    def get_response_create_at(self, obj):
        return obj.response.create_at.strftime("%d-%m-%Y %H:%M") if obj.response and obj.response.create_at else "-"
    get_response_create_at.short_description = "Response Created At"

    def get_response_update_at(self, obj):
        return obj.response.update_at.strftime("%d-%m-%Y %H:%M") if obj.response and obj.response.update_at else "-"
    get_response_update_at.short_description = "Response Updated At"

    def get_response_created_by(self, obj):
        return obj.response.created_by.username if obj.response and obj.response.created_by else "-"
    get_response_created_by.short_description = "Created By"

    def get_response_updated_by(self, obj):
        return obj.response.updated_by.username if obj.response and obj.response.updated_by else "-"
    get_response_updated_by.short_description = "Updated By"

    # Auto fill user (agar future me Meeting me bhi created_by chahiye ho)
    def save_model(self, request, obj, form, change):
        if not obj.pk and hasattr(obj, 'created_by'):
            obj.created_by = request.user
        if hasattr(obj, 'updated_by'):
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)


        

class FollowupAdmin(admin.ModelAdmin):
       
    list_display = (
        "id", 
        "response", 
        "get_response_contact_no", 
        "followup", 
        "get_response_comment",
        "get_response_business_name",
        "get_response_business_category",
        "get_response_locality",
        "get_response_city",
        "get_response_create_at",
        "get_response_update_at", 
        "get_response_created_by", 
        "get_response_updated_by"
    )
    list_filter = ("followup","response__city", "response__locality_city","response__business_category",)
    search_fields = ("response__id", "response__business_name", "response__contact_no")
    list_editable = ["followup"]
    list_per_page = 15

    def get_response_comment(self, obj):
        return obj.response.comment if obj.response else "-"
    get_response_comment.short_description = "Response Comment"

    def get_response_contact_no(self, obj):
        return obj.response.contact_no if obj.response else "-"
    get_response_contact_no.short_description = "Response Contact No"

    def get_response_city(self, obj):
        return obj.response.city if obj.response and obj.response.city else "-"
    get_response_city.short_description = "City"

    def get_response_locality(self, obj):
        return obj.response.locality_city if obj.response and obj.response.locality_city else "-"
    get_response_locality.short_description = "Locality"

    def get_response_business_name(self, obj):
        return obj.response.business_name if obj.response and obj.response.business_name else "-"
    get_response_business_name.short_description = "Business Name"

    def get_response_business_category(self, obj):
        return obj.response.business_category if obj.response and obj.response.business_category else "-"
    get_response_business_category.short_description = "Business Category"

    def get_response_create_at(self, obj):
        return obj.response.create_at.strftime("%d-%m-%Y %H:%M") if obj.response and obj.response.create_at else "-"
    get_response_create_at.short_description = "Response Created At"

    def get_response_update_at(self, obj):
        return obj.response.update_at.strftime("%d-%m-%Y %H:%M") if obj.response and obj.response.update_at else "-"
    get_response_update_at.short_description = "Response Updated At"

    def get_response_created_by(self, obj):
        return obj.response.created_by.username if obj.response and obj.response.created_by else "-"
    get_response_created_by.short_description = "Created By"

    def get_response_updated_by(self, obj):
        return obj.response.updated_by.username if obj.response and obj.response.updated_by else "-"
    get_response_updated_by.short_description = "Updated By"

    # Auto fill user (agar future me Meeting me bhi created_by chahiye ho)
    def save_model(self, request, obj, form, change):
        if not obj.pk and hasattr(obj, 'created_by'):
            obj.created_by = request.user
        if hasattr(obj, 'updated_by'):
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Followup, FollowupAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Response, ResponseAdmin)






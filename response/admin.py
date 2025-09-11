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
    exclude = ['created_by', 'updated_by']   # <-- Form me dropdown nahi dikhenga

    list_display = [
        'get_mr_id',
        'status',
        'meeting_follow',
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

    class Media:
        css = {
            'all': ('response/css/admin_cards.css',)
        }
        js = ('response/js/admin_cards.js',)


    list_filter = ['status', 'locality_city', 'city', 'business_category']
    list_editable = ['status', 'locality_city', 'city', 'business_category']
    search_fields = ['id', 'contact_no', 'comment']
    list_per_page = 15
    inlines = [MeetingInline, FollowupInline]

    def get_search_results(self, request, queryset, search_term):
        # Default Django search
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Agar search "MR" se start ho raha hai
        if search_term.upper().startswith("MR"):
            raw_id = search_term[2:]  # "MR" ke baad ka part nikal lo
            try:
                # Leading zeros hatao, number me convert karo
                num = int(raw_id.lstrip("0"))
                queryset |= self.model.objects.filter(id=num)
            except ValueError:
                pass

        return queryset, use_distinct

    def save_model(self, request, obj, form, change):
        if not obj.pk:   # New object hai
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def get_mr_id(self, obj):
        return f"MR{obj.id}"
    get_mr_id.short_description = "ID"

class MeetingAdminForm(forms.ModelForm):
    meeting_follow = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Meeting
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.response:
            instance.response.meeting_follow = self.cleaned_data['meeting_follow']
            instance.response.save()
        if commit:
            instance.save()
        return instance


class MeetingAdmin(admin.ModelAdmin):
    form = MeetingAdminForm
    list_display = ("id", "status", "get_response_meeting_follow", "get_response_comment")
    list_editable = ["status"]


class MeetingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_response_id",
        "get_response_contact_no",
        "status",
        "get_response_meeting_follow",   # ✅ ab method banayenge
        "get_response_comment",
        "get_response_business_name",
        "get_response_business_category",
        "get_response_locality",
        "get_response_city",
        "get_response_create_at",
        "get_response_update_at",
        "get_response_created_by",
        "get_response_updated_by",
    )
    list_filter = ("status", "response__city", "response__locality_city", "response__business_category")
    search_fields = ("response__id", "response__business_name", "response__contact_no")
    list_editable = ["status",]   # ✅ sirf model ka apna field
    list_per_page = 15

    def get_response_id(self, obj):
        return f"MR{obj.response.id}" if obj.response else "-"
    get_response_id.short_description = "Response ID"

    def get_response_contact_no(self, obj):
        return obj.response.contact_no if obj.response else "-"
    get_response_contact_no.short_description = "Response Contact No"

    def get_response_meeting_follow(self, obj):
        return obj.response.meeting_follow.strftime("%d-%m-%Y %H:%M") if obj.response and obj.response.meeting_follow else "-"
    get_response_meeting_follow.short_description = "Meeting Follow"

    def get_response_comment(self, obj):
        return obj.response.comment if obj.response else "-"
    get_response_comment.short_description = "Response Comment"

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

class FollowupAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_response_id",
        "get_response_contact_no",
        "status",
        "get_response_meeting_follow",   # ✅ ab method banayenge
        "get_response_comment",
        "get_response_business_name",
        "get_response_business_category",
        "get_response_locality",
        "get_response_city",
        "get_response_create_at",
        "get_response_update_at",
        "get_response_created_by",
        "get_response_updated_by",
    )
    list_filter = ("status", "response__city", "response__locality_city", "response__business_category")
    search_fields = ("response__id", "response__business_name", "response__contact_no")
    list_editable = ["status",]   # ✅ sirf model ka apna field
    list_per_page = 15

    def get_response_id(self, obj):
        return f"MR{obj.response.id}" if obj.response else "-"
    get_response_id.short_description = "Response ID"

    def get_response_contact_no(self, obj):
        return obj.response.contact_no if obj.response else "-"
    get_response_contact_no.short_description = "Response Contact No"

    def get_response_meeting_follow(self, obj):
        return obj.response.meeting_follow.strftime("%d-%m-%Y %H:%M") if obj.response and obj.response.meeting_follow else "-"
    get_response_meeting_follow.short_description = "Meeting Follow"

    def get_response_comment(self, obj):
        return obj.response.comment if obj.response else "-"
    get_response_comment.short_description = "Response Comment"

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

admin.site.register(Followup, FollowupAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Response, ResponseAdmin)






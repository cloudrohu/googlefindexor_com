from django.contrib import admin
from django import forms
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Response, Meeting, Followup


# ------------------------------
#  Import Export Resources
# ------------------------------
class ResponseResource(resources.ModelResource):
    class Meta:
        model = Response
        fields = (
            "id", "status", "contact_persone", "contact_no",
            "comment", "meeting_follow", "business_name",
            "business_category", "locality_city", "city",
            "created_by", "updated_by", "create_at", "update_at"
        )


class MeetingResource(resources.ModelResource):
    class Meta:
        model = Meeting
        fields = (
            "id", "status", "response", "meeting_follow",
            "created_by", "updated_by", "create_at", "update_at"
        )


class FollowupResource(resources.ModelResource):
    class Meta:
        model = Followup
        fields = (
            "id", "status", "response", "follow_up",
            "created_by", "updated_by", "create_at", "update_at"
        )


# ------------------------------
#  Inlines
# ------------------------------
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


# ------------------------------
#  Response Admin
# ------------------------------
class ResponseAdminForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = '__all__'

    def clean_contact_no(self):
        contact_no = self.cleaned_data.get('contact_no')
        if contact_no:
            contact_no = contact_no.replace(" ", "")
        return contact_no


class ResponseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ResponseResource
    form = ResponseAdminForm

    exclude = ['created_by', 'updated_by']

    list_display = [
        'get_mr_id',
        'status',
        'contact_persone',
        'contact_no',
        'comment',
        'meeting_follow',
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

    list_filter = ['status', 'meeting_follow', 'locality_city', 'city', 'business_category']
    list_editable = ['status', 'locality_city', 'city', 'business_category']
    search_fields = ['id', 'contact_no', 'comment']
    list_per_page = 15
    inlines = [MeetingInline, FollowupInline]

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term.upper().startswith("MR"):
            raw_id = search_term[2:]
            try:
                num = int(raw_id.lstrip("0"))
                queryset |= self.model.objects.filter(id=num)
            except ValueError:
                pass
        return queryset, use_distinct

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def get_mr_id(self, obj):
        return f"MR{obj.id}"
    get_mr_id.short_description = "ID"


# ------------------------------
#  Meeting Admin
# ------------------------------
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


class MeetingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = MeetingResource
    form = MeetingAdminForm

    list_display = (
        "id",
        "status",
        "get_response_id",
        "get_response_contact_persone",
        "get_response_contact_no",
        "get_response_comment",
        "get_response_meeting_follow",
        "get_response_business_name",
        "get_response_business_category",
        "get_response_locality",
        "get_response_city",
        "get_response_create_at",
        "get_response_update_at",
        "get_response_created_by",
        "get_response_updated_by",
    )

    class Media:
        css = {
            'all': ('response/css/meeting_cards.css',)
        }
        js = ('response/js/meeting_cards.js',)

    list_filter = ("status", "response__city", "response__locality_city", "response__business_category")
    search_fields = ("response__id", "response__business_name", "response__contact_no")
    list_editable = ["status",]
    list_per_page = 15

    def get_response_id(self, obj):
        return f"MR{obj.response.id}" if obj.response else "-"
    get_response_id.short_description = "Response ID"

    def get_response_contact_no(self, obj):
        return obj.response.contact_no if obj.response else "-"
    def get_response_contact_persone(self, obj):
        return obj.response.contact_persone if obj.response else "-"
    def get_response_meeting_follow(self, obj):
        return obj.response.meeting_follow.strftime("%d-%m-%Y %H:%M") if obj.response and obj.response.meeting_follow else "-"
    def get_response_comment(self, obj):
        return obj.response.comment if obj.response else "-"
    def get_response_city(self, obj):
        return obj.response.city if obj.response and obj.response.city else "-"
    def get_response_locality(self, obj):
        return obj.response.locality_city if obj.response and obj.response.locality_city else "-"
    def get_response_business_name(self, obj):
        return obj.response.business_name if obj.response else "-"
    def get_response_business_category(self, obj):
        return obj.response.business_category if obj.response else "-"
    def get_response_create_at(self, obj):
        return obj.response.create_at.strftime("%d-%m-%Y %H:%M") if obj.response and obj.response.create_at else "-"
    def get_response_update_at(self, obj):
        return obj.response.update_at.strftime("%d-%m-%Y %H:%M") if obj.response and obj.response.update_at else "-"
    def get_response_created_by(self, obj):
        return obj.response.created_by.username if obj.response and obj.response.created_by else "-"
    def get_response_updated_by(self, obj):
        return obj.response.updated_by.username if obj.response and obj.response.updated_by else "-"


# ------------------------------
#  Followup Admin
# ------------------------------
class FollowupAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = FollowupResource

    list_display = (
        "id",
        "status",
        "get_response_id",
        "get_response_contact_persone",
        "get_response_contact_no",
        "get_response_comment",
        "get_response_meeting_follow",
        "get_response_business_name",
        "get_response_business_category",
        "get_response_locality",
        "get_response_city",
        "get_response_create_at",
        "get_response_update_at",
        "get_response_created_by",
        "get_response_updated_by",
    )

    class Media:
        css = {
            'all': ('response/css/meeting_cards.css',)
        }
        js = ('response/js/meeting_cards.js',)

    list_filter = ("status", "response__city", "response__locality_city", "response__business_category")
    search_fields = ("response__id", "response__business_name", "response__contact_no")
    list_editable = ["status",]
    list_per_page = 15

    def get_response_id(self, obj):
        return f"MR{obj.response.id}" if obj.response else "-"
    def get_response_contact_no(self, obj):
        return obj.response.contact_no if obj.response else "-"
    def get_response_contact_persone(self, obj):
        return obj.response.contact_persone if obj.response else "-"
    def get_response_meeting_follow(self, obj):
        return obj.response.meeting_follow.strftime("%d-%m-%Y %H:%M") if obj.response and obj.response.meeting_follow else "-"
    def get_response_comment(self, obj):
        return obj.response.comment if obj.response else "-"
    def get_response_city(self, obj):
        return obj.response.city if obj.response and obj.response.city else "-"
    def get_response_locality(self, obj):
        return obj.response.locality_city if obj.response and obj.response.locality_city else "-"
    def get_response_business_name(self, obj):
        return obj.response.business_name if obj.response else "-"
    def get_response_business_category(self, obj):
        return obj.response.business_category if obj.response else "-"
    def get_response_create_at(self, obj):
        return obj.response.create_at.strftime("%d-%m-%Y %H:%M") if obj.response and obj.response.create_at else "-"
    def get_response_update_at(self, obj):
        return obj.response.update_at.strftime("%d-%m-%Y %H:%M") if obj.response and obj.response.update_at else "-"
    def get_response_created_by(self, obj):
        return obj.response.created_by.username if obj.response and obj.response.created_by else "-"
    def get_response_updated_by(self, obj):
        return obj.response.updated_by.username if obj.response and obj.response.updated_by else "-"


# ------------------------------
#  Register Admins
# ------------------------------
admin.site.register(Response, ResponseAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Followup, FollowupAdmin)

from django.contrib import admin
from django.utils.html import format_html
from .models import Campaign


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "date",
        "status",
        "messaging_conversations_started",
        "spent",
        "cost_per_conversation",
        "thumbnail_tag",   # 👈 Thumbnail preview column
    )
    readonly_fields = ("cost_per_conversation", "thumbnail_tag")  # form me bhi dikhega

    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="width:60px; height:60px; object-fit:cover; border-radius:6px;" />',
                obj.thumbnail.url
            )
        return "—"
    thumbnail_tag.short_description = "Thumbnail"
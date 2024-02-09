
import admin_thumbnails
from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from .models import *

admin.site.register(Find_Form,)
admin.site.register(Call_Status,)
admin.site.register(SocialSite,)
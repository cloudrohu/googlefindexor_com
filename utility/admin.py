
import admin_thumbnails
from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from .models import *

admin.site.register(City,)
admin.site.register(Locality,)
admin.site.register(Sub_Locality,)
admin.site.register(Find_Form,)
admin.site.register(Call_Status,)
admin.site.register(SocialSite,)
admin.site.register(Googlemap_Status,)
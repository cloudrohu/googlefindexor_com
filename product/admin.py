import admin_thumbnails
from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from product import models
from product.models import *



@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    list_display = ['id']
    model = Images
    readonly_fields = ('id',)
    extra = 1

class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True

    
@admin_thumbnails.thumbnail('image')
class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('id','tree_actions', 'indented_title', 'image_thumbnail',
                    'related_products_count', 'related_products_cumulative_count',)
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

class CategoryApproxInline(admin.TabularInline):
    model = Approx
    extra = 1
    show_change_link = True

class CompanySocialInline(admin.TabularInline):
    model = SocialLink
    extra = 1
    show_change_link = True

class CompanyErrorInline(admin.TabularInline):
    model = Error
    extra = 1
    show_change_link = True

class Follow_UpInline(admin.TabularInline):
    model = Follow_Up
    extra = 1
    show_change_link = True

class MeetingInline(admin.TabularInline):
    model = Meeting
    extra = 1
    show_change_link = True

class VisitInline(admin.TabularInline):
    model = Visit
    extra = 1
    show_change_link = True


class FaqInline(admin.TabularInline):
    model = Faq
    extra = 1
    show_change_link = True

class ApproxAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'locality','city', 'title', ]
    list_filter = [ 'category', 'locality','city', ]

    search_fields = ['title']
    list_per_page = 30 



@admin_thumbnails.thumbnail('image')
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image','title','id','image_thumbnail']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_tag','category','call_status', 'find_form', 'contact_person', 'contact_no', 'email','city','locality','address','keywords', 'website', 'create_at','update_at','updated_by']
    list_filter = ['category','category','call_status', 'find_form','city','locality',]
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline,ProductVariantsInline,CompanySocialInline,CompanyErrorInline,Follow_UpInline,MeetingInline,VisitInline,FaqInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','subject','comment', 'product','status','create_at','rate','ip']
    list_filter = ['status']
    list_editable = ['status']
    readonly_fields = ('subject','comment','ip','user','product','rate','id')

class ColorAdmin(admin.ModelAdmin):
    list_display = ['name','code','color_tag']

class SizeAdmin(admin.ModelAdmin):
    list_display = ['name','code']


class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title','product','color','size','price','quantity','image_tag']

class ProductLangugaeAdmin(admin.ModelAdmin):
    list_display = ['title','lang','slug']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['lang']

class CategoryLangugaeAdmin(admin.ModelAdmin):
    list_display = ['title','lang','slug']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['lang']

admin.site.register(Category,CategoryAdmin2)
admin.site.register(Product,ProductAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Images,ImagesAdmin)
admin.site.register(Color,ColorAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(City,)
admin.site.register(Variants,VariantsAdmin)



admin.site.register(SocialLink)
admin.site.register(Error,)

admin.site.register(Follow_Up)
admin.site.register(Meeting)
admin.site.register(Visit)
admin.site.register(Locality)
admin.site.register(Approx,ApproxAdmin,)
admin.site.register(Society_Building)

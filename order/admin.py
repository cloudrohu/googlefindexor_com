from django.contrib import admin

# Register your models here.
from order.models import ShopCart, Order, OrderProduct


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['product','user','quantity','price','amount' ]
    list_filter = ['user']

class OrderProductline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product','price','quantity','amount')
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','first_name', 'last_name','phone','city','total','status','create_at']
    list_filter = ['status']
    list_editable = ['status']
    readonly_fields = ('user','address','city','country','phone','first_name','ip', 'last_name','phone','city','total')
    can_delete = False
    inlines = [OrderProductline]

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product','price','quantity','amount','status','create_at']
    list_filter = ['user']
    list_editable = ['status']

admin.site.register(ShopCart,ShopCartAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)
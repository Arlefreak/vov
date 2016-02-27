from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
from .models import Product, Adress, Client, Order, ShoppingCartProduct, Category, ProductImages
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 0

class ProductAdmin(OrderedModelAdmin, ImportExportModelAdmin):
    list_display = (
        'move_up_down_links',
        'sku',
        'name',
        'inventory',
        'price',
        'status',
        'date',
        'image_img'
    )
    list_editable= ('price','status', 'inventory',)
    list_display_links = ('sku', 'name')
    inlines = [ ProductImagesInline ]
    list_filter = ('category',)
    search_fields = ('name', 'sku',)
    resource_class = ProductResource

class AdressAdmin(admin.ModelAdmin):
    list_display = ('client', 'name', 'type', 'default', 'country', 'zipcode')

class ClientAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_first_name', 'get_last_name', 'get_email')
    def get_username(self, obj):
        return obj.user.username
    def get_first_name(self, obj):
        return obj.user.first_name
    def get_last_name(self, obj):
        return obj.user.last_name
    def get_email(self, obj):
        return obj.user.email
    get_username.short_description = "Username"
    get_first_name.short_description = "Firstname"
    get_last_name.short_description = "Lastname"
    get_email.short_description = "Email"
    get_username.admin_order_field = 'user__username'
    get_first_name.admin_order_field = 'user__first_name'
    get_last_name.admin_order_field = 'user__last_name'
    get_email.admin_order_field = 'user__email'

class OrderAdmin(admin.ModelAdmin):
    list_display = ('sku', 'client', 'shippingAdress', 'billingAdress', 'items_subTotal','shipping_cost','taxes_cost', 'total','shipping_carrier', 'shipping_tracking','date', 'updated', 'status')

class ShoppingCartProductAdmin(admin.ModelAdmin):
    list_display = ('client', 'product', 'cuantity')

admin.site.register(Product, ProductAdmin)
admin.site.register(Adress, AdressAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Category)
admin.site.register(ShoppingCartProduct, ShoppingCartProductAdmin)

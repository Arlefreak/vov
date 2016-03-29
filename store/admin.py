from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
from .models import Product, Category, ProductImages, ProductVariant, Press, PressImage, VideoPress, Stores, Store, StoreImage
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from solo.admin import SingletonModelAdmin


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

class ProductVariantResource(resources.ModelResource):
    class Meta:
        model = ProductVariant

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class productVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0

class productImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 0

class storeImagesInline(admin.TabularInline):
    model = StoreImage
    extra = 0

class pressImageInline(admin.TabularInline):
    model = PressImage
    extra = 0
class pressVideoInline(admin.TabularInline):
    model = VideoPress
    extra = 0

class ProductAdmin(OrderedModelAdmin, ImportExportModelAdmin):
    list_display = (
        'move_up_down_links',
        'sku',
        'name',
        'stock',
        'price',
        'status',
        'date',
        'image_img',
    )
    list_editable= ('price', )
    list_display_links = ('sku', 'name')
    inlines = [ productVariantInline ]
    list_filter = ('category',)
    search_fields = ('name', 'sku',)
    resource_class = ProductResource

class PressAdmin(OrderedModelAdmin, ImportExportModelAdmin):
    list_display = (
        'move_up_down_links',
        'publish',
        'slug',
        'title',
        'date',
    )
    list_editable= ('publish', )
    list_display_links = ('slug', 'title')
    inlines = [ pressImageInline, pressVideoInline]
    search_fields = ('title', 'slug',)

class ProductVariantAdmin(OrderedModelAdmin, ImportExportModelAdmin):
    list_display = (
        'move_up_down_links',
        'product',
        'sku',
        'inventory',
        'date',
        'image_img',
    )
    list_editable= ('inventory',)
    list_display_links = ('sku', 'product', 'image_img')
    inlines = [ productImagesInline ]
    list_filter = ('product',)
    search_fields = ('name', 'sku',)
    resource_class = ProductVariantResource

class CategoryAdmin(OrderedModelAdmin, ImportExportModelAdmin):
    list_display = (
        'move_up_down_links',
        'sku',
        'name',
        'image_img',
    )
    list_display_links = ('sku', 'name', 'image_img')
    search_fields = ('name', 'sku',)
    resource_class = CategoryResource

class StoresAdmin(OrderedModelAdmin):
    list_display = (
        'move_up_down_links',
        'publish',
        'slug',
        'name',
        'adress',
        'mail',
    )
    list_display_links = ('slug', 'name', 'adress', 'mail')
    list_editable= ('publish',)
    search_fields = ('name', 'slug',)

class StoreAdmin(SingletonModelAdmin):
    list_display = (
        'name',
        'small_description',
        'mail',
        'phone',
    )
    list_display_links = ('name', 'small_description', 'mail', 'phone')
    inlines = [ storeImagesInline ]

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
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Press, PressAdmin)
admin.site.register(Stores, StoresAdmin)
admin.site.register(Store, StoreAdmin)
# admin.site.register(Adress, AdressAdmin)
# admin.site.register(Client, ClientAdmin)
# admin.site.register(Order, OrderAdmin)
# admin.site.register(ShoppingCartProduct, ShoppingCartProductAdmin)

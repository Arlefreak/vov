from django.contrib import admin
from django.urls import reverse
from ordered_model.admin import OrderedModelAdmin
from .models import Product, Category, ProductImages, ProductVariant, Press, PressImage, VideoPress, Stores, Store, StoreImage, ProductVideo
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from solo.admin import SingletonModelAdmin
import nested_admin
from embed_video.admin import AdminVideoMixin

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

class ProductVariantResource(resources.ModelResource):
    class Meta:
        model = ProductVariant

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category

class productImagesInline(nested_admin.NestedStackedInline):
    model = ProductImages
    extra = 1

class productVideosInline(nested_admin.NestedStackedInline):
    model = ProductVideo
    extra = 1

class productVariantInline(nested_admin.NestedStackedInline):
    model = ProductVariant
    extra = 0
    inlines = [productImagesInline, productVideosInline]

class storeImagesInline(admin.TabularInline):
    model = StoreImage
    extra = 0

class pressImageInline(admin.TabularInline):
    model = PressImage
    extra = 0

class pressVideoInline(admin.TabularInline):
    model = VideoPress
    extra = 0

@admin.register(Product)
class ProductAdmin(nested_admin.NestedModelAdmin, OrderedModelAdmin, ImportExportModelAdmin):
    list_display = (
        'move_up_down_links',
        'name',
        'price',
        # 'status',
        # 'date',
        'admin_description',
        # 'image_img',
        'view_on_site',
    )
    list_editable= ('price', )
    list_display_links = ('name', 'admin_description')
    inlines = [ productVariantInline ]
    list_filter = ('category',)
    search_fields = ('name', 'sku',)
    resource_class = ProductResource
    save_on_top = True
    def admin_description(self, obj):
        return '<div style="max-width:300px">%s<div>' % obj.description
    def view_on_site(self, obj):
        url = reverse('products', kwargs={'category_name': obj.category.sku })
        return '<a class="button" target="_blank" href="http://vvvvovvvv.com%s">View</a>' % url

    view_on_site.allow_tags = True
    admin_description.allow_tags = True
    view_on_site.short_description = 'View on Site'
    admin_description.short_description = 'Description'

@admin.register(Press)
class PressAdmin(OrderedModelAdmin, ImportExportModelAdmin):
    list_display = (
        'move_up_down_links',
        'publish',
        'title',
        'date_article',
        'date',
        'view_on_site',
    )
    list_editable= ('publish', 'date_article')
    list_display_links = ('title', )
    inlines = [ pressImageInline, pressVideoInline]
    search_fields = ('title', 'slug',)
    def view_on_site(self, obj):
        url = reverse('press_single', kwargs={'press_name': obj.slug})
        return '<a class="button" target="_blank" href="http://vvvvovvvv.com%s">View</a>' % url
    view_on_site.allow_tags = True

@admin.register(ProductVariant)
class ProductVariantAdmin(OrderedModelAdmin, ImportExportModelAdmin):
    list_display = (
        'move_up_down_links',
        'parent_product',
        'product_variant',
        'inventory',
        'date',
        'image_img',
        'view_on_site',
    )
    list_editable= ('inventory',)
    list_display_links = ('parent_product', 'product_variant', )
    inlines = [ productImagesInline, productVideosInline ]
    list_filter = ('product',)
    search_fields = ('name', 'sku',)
    resource_class = ProductVariantResource
    def product_variant(self, obj):
        return obj.name
    def parent_product(self, obj):
        return obj.product.name
    def view_on_site(self, obj):
        url = reverse('product', kwargs={'category_name': obj.product.category.sku, 'product_name': obj.product.sku, 'variant_name': obj.sku})
        return '<a class="button" target="_blank" href="http://vvvvovvvv.com%s">View</a>' % url
    view_on_site.allow_tags = True
    parent_product.short_description = 'Product'
    product_variant.short_description = 'Variant'

@admin.register(Category)
class CategoryAdmin(OrderedModelAdmin, ImportExportModelAdmin):
    list_display = (
        'move_up_down_links',
        'publish',
        'name',
        'admin_description',
        'image_img',
        'view_on_site',
    )
    list_display_links = ('name', 'image_img')
    list_editable = ('publish',)
    search_fields = ('name',)
    resource_class = CategoryResource
    def admin_description(self, obj):
        return '<div style="max-width:300px">%s<div>' % obj.description
    def view_on_site(self, obj):
        url = reverse('products', kwargs={'category_name': obj.sku})
        return '<a class="button" target="_blank" href="http://vvvvovvvv.com%s">View</a>' % url
    view_on_site.allow_tags = True
    admin_description.allow_tags = True

@admin.register(Store)
class StoreAdmin(SingletonModelAdmin):
    list_display = (
        'name',
        'small_description',
        'mail',
        'phone',
    )
    list_display_links = ('name', 'small_description', 'mail', 'phone')
    inlines = [ storeImagesInline ]

@admin.register(ProductImages)
class ProductImageAdmin(OrderedModelAdmin):
    list_display = (
        'move_up_down_links',
        'parent_product',
        'product_variant',
        'image_img',
        'view_on_site',
    )
    list_display_links = (
        'parent_product',
        'product_variant',
    )
    list_filter = (
        'product__product',
        'product',
    )
    search_fields = (
        'name',
        'product',
    )
    def product_variant(self, obj):
        return obj.product
    def parent_product(self, obj):
        return obj.product.product
    def view_on_site(self, obj):
        url = reverse('product', kwargs={'category_name': obj.product.product.category.sku, 'product_name': obj.product.product.sku, 'variant_name': obj.product.sku})
        return '<a class="button" target="_blank" href="http://vvvvovvvv.com%s">View</a>' % url
    parent_product.short_description = 'Product'
    product_variant.short_description = 'Variant'
    view_on_site.allow_tags = True

@admin.register(ProductVideo)
class ProductVideoAdmin(AdminVideoMixin, OrderedModelAdmin):
    list_display = (
        'move_up_down_links',
        'order',
        'name',
        'product',
    )
    list_display_links = (
        'order',
        'name',
        'product',
    )
    list_filter = (
        'product__product',
        'product',
    )
    search_fields = (
        'name',
        'product',
    )


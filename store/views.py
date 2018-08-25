# -*- coding: utf-8 -*-
from bleach import clean
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.html import strip_tags
from rest_framework import filters, permissions, viewsets
from store.models import (Adress, Category, Order, Press, Product,
                          ProductImages, ProductVariant, ShoppingCartProduct,
                          Store, StoreImage, Stores)
from store.serializers import (AdressSerializer, CategorySerializer,
                               OrderSerializer, ProductImageSerializer,
                               ProductSerializer,
                               ShoppingCartProductSerializer, UserSerializer)
from taggit.models import Tag
from taggit_serializer.serializers import TaggitSerializer

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset           = Product.objects.all()
#     serializer_class   = ProductSerializer
#     filter_backends = (filters.DjangoFilterBackend,)
#     filter_fields = ('category','category__name', 'status')
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

# class ProductImagesViewset(viewsets.ModelViewSet):
#     queryset           = ProductImages.objects.all()
#     serializer_class   = ProductImageSerializer
#     filter_backends = (filters.DjangoFilterBackend,)
#     filter_fields = ('product','product__name',)
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

# class CategoryViewset(viewsets.ModelViewSet):
#     queryset           = Category.objects.all()
#     serializer_class   = CategorySerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

# class UserViewset(viewsets.ModelViewSet):
#     queryset           = User.objects.all()
#     serializer_class   = UserSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

# class ShoppingCartProductViewset(viewsets.ModelViewSet):
#     queryset           = ShoppingCartProduct.objects.all()
#     serializer_class   = ShoppingCartProductSerializer
#     filter_backends = (filters.DjangoFilterBackend,)
#     filter_fields = ('client',)
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

# class OrderViewSet(viewsets.ModelViewSet):
#     queryset           = Order.objects.all()
#     serializer_class   = OrderSerializer
#     filter_backends = (filters.DjangoFilterBackend,)
#     filter_fields = ('client',)
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

# class AdressViewSet(viewsets.ModelViewSet):
#     queryset           = Adress.objects.all()
#     serializer_class   = AdressSerializer
#     filter_backends = (filters.DjangoFilterBackend,)
#     filter_fields = ('client',)
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

# class TaggitViewSet(viewsets.ModelViewSet):
#     queryset           = Tag.objects.all()
#     serializer_class   = TaggitSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


def HomeView(request):
    p_list = ""
    single = ""
    title = "vov"
    description = "Somos productores de accesorios únicos para hombres y mujeres que buscan utilidad y buen diseño, lo necesario para acompañar su rutina diaria."
    previewImage = Store.get_solo().image.url
    template_name = "home.html"
    context = {
        'p_list': p_list,
        'single': single,
        'title': title,
        'description': description,
        'previewImage': previewImage
    }
    return render(request, template_name, context)


def AboutView(request):
    p_list = StoreImage.objects.all()
    single = ""
    footer = ProductImages.objects.order_by('?').first()
    title = "About"
    description = "Somos productores de accesorios únicos para hombres y mujeres que buscan utilidad y buen diseño, lo necesario para acompañar su rutina diaria."
    previewImage = Store.get_solo().image.url
    template_name = "about.html"
    context = {
        'p_list': p_list,
        'single': single,
        'title': title,
        'description': description,
        'previewImage': previewImage
    }
    return render(request, template_name, context)


def CategoryListView(request):
    p_list = Category.objects.order_by('order').filter(publish=True)
    single = ""
    footer = ProductImages.objects.order_by('?').first()
    title = "Catalog"
    description = "Somos productores de accesorios únicos para hombres y mujeres que buscan utilidad y buen diseño, lo necesario para acompañar su rutina diaria."
    previewImage = Store.get_solo().image.url
    template_name = "category__list.html"
    context = {
        'p_list': p_list,
        'single': single,
        'title': title,
        'description': description,
        'previewImage': previewImage
    }
    return render(request, template_name, context)


def ColaboracionesView(request):
    p_list = Product.objects.filter(category__sku='colaboraciones')
    single = get_object_or_404(Category, sku='colaboraciones')
    title = single.name
    description = strip_tags(single.description)
    previewImage = Store.get_solo().image.url
    template_name = "colabs__list.html"
    context = {
        'p_list': p_list,
        'single': single,
        'title': title,
        'description': description,
        'previewImage': previewImage
    }
    return render(request, template_name, context)


def ColaboracionesSingleView(request, category_name, product_name):
    single = get_object_or_404(Product, sku=product_name)
    p_list = ProductVariant.objects.filter(product__sku=product_name)
    title = single.name
    description = strip_tags(single.description)
    previewImage = Store.get_solo().image.url
    template_name = "colabs__single.html"
    context = {
        'p_list': p_list,
        'single': single,
        'title': title,
        'description': description,
        'previewImage': previewImage
    }
    return render(request, template_name, context)


def ProductsListView(request, category_name):
    p_list = ProductVariant.objects.filter(
        product__category__sku=category_name)
    if (p_list is None):
        p_list = Product.objects.filter(category__sku=category_name)
    single = get_object_or_404(Category, sku=category_name)
    title = single.name
    description = clean(single.description, strip=True)
    description = description.encode('utf-8')
    description = description.decode('utf-8')
    if (len(p_list) <= 1):
        return redirect(
            'product',
            category_name=single.sku,
            product_name=p_list[0].product.sku,
            variant_name=p_list[0].sku)
    previewImage = Store.get_solo().image.url
    previewImage = str(
        ProductImages.objects.filter(product__sku=p_list[0].sku).first())
    template_name = "products__list.html"
    context = {
        'p_list': p_list,
        'single': single,
        'title': title,
        'description': description,
        'previewImage': previewImage
    }
    return render(request, template_name, context)


def ProductsSingleView(request, category_name, product_name, variant_name):
    # p_list = get_object_or_404(Product, sku=product_name, category__sky=category_name)
    p_list = get_object_or_404(
        ProductVariant, sku=variant_name, product__sku=product_name)
    v_list = p_list.video_gallery
    p_list = p_list.gallery
    single = get_object_or_404(Product, sku=product_name)
    title = single.name
    description = strip_tags(single.description)
    previewImage = str(
        ProductImages.objects.filter(product__sku=variant_name).first())
    template_name = "products__single.html"
    context = {
        'p_list': p_list,
        'v_list': v_list,
        'single': single,
        'title': title,
        'description': description,
        'previewImage': previewImage
    }
    return render(request, template_name, context)


def PressListView(request):
    p_list = Press.objects.order_by('order').filter(publish=True)
    single = ""
    footer = ProductImages.objects.order_by('?').first()
    title = "Prensa"
    description = "Somos productores de accesorios únicos para hombres y mujeres que buscan utilidad y buen diseño, lo necesario para acompañar su rutina diaria."
    previewImage = Store.get_solo().image.url
    template_name = "press__list.html"
    context = {
        'p_list': p_list,
        'single': single,
        'title': title,
        'description': description,
        'previewImage': previewImage
    }
    return render(request, template_name, context)


def PressSingleView(request, press_name):
    p_list = get_object_or_404(Press, slug=press_name)
    p_list = p_list.gallery
    videos = get_object_or_404(Press, slug=press_name)
    videos = videos.videos
    single = get_object_or_404(Press, slug=press_name)
    footer = ProductImages.objects.order_by('?').first()
    title = "vov - prensa"
    description = "Somos productores de accesorios únicos para hombres y mujeres que buscan utilidad y buen diseño, lo necesario para acompañar su rutina diaria."
    previewImage = Store.get_solo().image.url
    template_name = "press__single.html"
    context = {
        'p_list': p_list,
        'single': single,
        'title': title,
        'description': description,
        'previewImage': previewImage,
        'videos': videos
    }
    return render(request, template_name, context)


def ContactView(request):
    p_list = Stores.objects.order_by('order').filter(publish=True)
    single = ""
    footer = ProductImages.objects.order_by('?').first()
    title = "Contact"
    description = "Somos productores de accesorios únicos para hombres y mujeres que buscan utilidad y buen diseño, lo necesario para acompañar su rutina diaria."
    template_name = "contact.html"
    previewImage = Store.get_solo().image.url
    context = {
        'p_list': p_list,
        'single': single,
        'title': title,
        'description': description,
        'previewImage': previewImage,
    }
    return render(request, template_name, context)

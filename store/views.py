from store.models import Product, ProductImages, Category, ShoppingCartProduct, Order, Adress, ProductVariant
from store.serializers import ProductSerializer, ProductImageSerializer, CategorySerializer, \
    ShoppingCartProductSerializer, OrderSerializer, AdressSerializer, UserSerializer
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import filters
from taggit.models import Tag
from taggit_serializer.serializers import TaggitSerializer
# from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

class ProductViewSet(viewsets.ModelViewSet):
    queryset           = Product.objects.all()
    serializer_class   = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('category','category__name', 'status')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class ProductImagesViewset(viewsets.ModelViewSet):
    queryset           = ProductImages.objects.all()
    serializer_class   = ProductImageSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('product','product__name',)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class CategoryViewset(viewsets.ModelViewSet):
    queryset           = Category.objects.all()
    serializer_class   = CategorySerializer 
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class UserViewset(viewsets.ModelViewSet):
    queryset           = User.objects.all()
    serializer_class   = UserSerializer 
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class ShoppingCartProductViewset(viewsets.ModelViewSet):
    queryset           = ShoppingCartProduct.objects.all()
    serializer_class   = ShoppingCartProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('client',)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class OrderViewSet(viewsets.ModelViewSet):
    queryset           = Order.objects.all()
    serializer_class   = OrderSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('client',)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class AdressViewSet(viewsets.ModelViewSet):
    queryset           = Adress.objects.all()
    serializer_class   = AdressSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('client',)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class TaggitViewSet(viewsets.ModelViewSet):
    queryset           = Tag.objects.all()
    serializer_class   = TaggitSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

def HomeView (request):
    p_list = ""
    single = ""
    title  = "vov"
    description = "store"
    template_name = "home.html"
    context = {'p_list': p_list, 'single': single, 'title': title, 'description': description}
    return render(request, template_name, context)

def AboutView(request):
    p_list = ""
    single = ""
    title  = "vov - about"
    description = "store"
    template_name = "about.html"
    context = {'p_list': p_list, 'single': single, 'title': title, 'description': description}
    return render(request, template_name, context)

def CategoryListView(request):
    p_list = Category.objects.order_by('order')
    single = ""
    title  = "vov - catalog"
    description = "store"
    template_name = "category__list.html"
    context = {'p_list': p_list, 'single': single, 'title': title, 'description': description}
    return render(request, template_name, context)

def ProductsListView(request, category_name):
    p_list = ProductVariant.objects.filter(product__category__sku=category_name)
    if(p_list is None):
        p_list = Product.objects.filter(category__sku=category_name)
    single = get_object_or_404(Category, sku=category_name)
    title  = "vov - cat"
    description = "store"
    template_name = "products__list.html"
    context = {'p_list': p_list, 'single': single, 'title': title, 'description': description}
    return render(request, template_name, context)

def ProductsSingleView(request, category_name, product_name, variant_name):
    p_list = get_object_or_404(ProductVariant, sku=variant_name)
    p_list = p_list.gallery
    single = get_object_or_404(Product, sku=product_name)
    title  = "vov - product"
    description = "store"
    template_name = "products__single.html"
    context = {'p_list': p_list, 'single': single, 'title': title, 'description': description}
    return render(request, template_name, context)

def PressListView(request):
    p_list = ""
    single = ""
    title  = "vov - prensa"
    description = "store"
    template_name = "press__list.html"
    context = {'p_list': p_list, 'single': single, 'title': title, 'description': description}
    return render(request, template_name, context)

def PressSingleView(request):
    p_list = ""
    single = ""
    title  = "vov - prensa"
    description = "store"
    template_name = "press__single.html"
    context = {'p_list': p_list, 'single': single, 'title': title, 'description': description}
    return render(request, template_name, context)

def ContactView(request):
    p_list = ""
    single = ""
    title  = "vov"
    description = "store - contacto"
    template_name = "contact.html"
    context = {'p_list': p_list, 'single': single, 'title': title, 'description': description}
    return render(request, template_name, context)

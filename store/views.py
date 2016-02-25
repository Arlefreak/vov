from store.models import Product, ProductImages, Category, ShoppingCartProduct, Order, Adress
from store.serializers import ProductSerializer, ProductImageSerializer, CategorySerializer, \
    ShoppingCartProductSerializer, OrderSerializer, AdressSerializer, UserSerializer
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import filters
from taggit.models import Tag
from taggit_serializer.serializers import TaggitSerializer
from django.views.generic import TemplateView
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

class HomeView (TemplateView):
    template_name = "home.html"

class AboutView(TemplateView):
    template_name = "about.html"

class ContactoView(TemplateView):
    template_name = "contact.html"

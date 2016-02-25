from rest_framework                import serializers
from django.contrib.auth.models    import User
from taggit_serializer.serializers import (TagListSerializerField, TaggitSerializer)
from store.models               import Product, Category, ProductImages, ShoppingCartProduct, Order, Adress, Client
from taggit.models                 import Tag

class ProductSerializer(TaggitSerializer,serializers.ModelSerializer):
    tags = TagListSerializerField(required=False)
    category = serializers.StringRelatedField()
    class Meta:
        model = Product
        fields = ('pk','sku','name','image','description','price','discount','inventory','status','tags','category','date','updated','order','url')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk','name','image','date','updated','order',)

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ('pk','product', 'name', 'image', 'order', 'date', 'updated',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk','username','first_name', 'last_name', 'email')
    def create(self, validated_data):
        client_data = validated_data.pop('client', None)
        user = super(UserSerializer, self).create(validated_data)
        self.create_or_update_client(user, client_data)
        return user
    def update(self, instance, validated_data):
        client_data = validated_data.pop('client', None)
        self.create_or_update_client(instance, client_data)
        return super(UserSerializer, self).update(instance, validated_data)
    def create_or_update_profile(self, user, client_data):
        client, created = Client.objects.get_or_create(user=user, defaults=client_data)
        if not created and client_data is not None:
            super(UserSerializer, self).update(client, client_data)

class ShoppingCartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCartProduct
        fields = ('pk','client', 'product', 'cuantity')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('pk','sku','client', 'shippingAdress', 'billingAdress', 'items_subTotal', 'shipping_cost', 'total', 'shipping_carrier', 'shipping_tracking', 'date', 'updated', 'status',)

class AdressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adress
        fields = ('pk','client', 'name', 'type', 'default', 'firstname', 'lastname', 'adress_line1', 'adress_line2', 'city', 'state_province', 'country', 'zipcode', 'phone_number', 'date',)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('pk','name',)


from dataclasses import field
from decimal import Decimal
from pyexpat import model
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import OrderItem, Product, Review, Order, Cart, CartItem


class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(
        method_name="calculate_tax")

    def calculate_tax(self, product):
        return product.price * Decimal(1.1)

    class Meta:
        model = Product
        fields = ['id', 'name',
                  'description', 'color', 'price', 'image', 'price_with_tax']


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'date', 'reviewer', 'description',
                  'rating']
    # ensures that the product_id is passed to the serializer and therefore the view, don't forget to add the product_id to the context in the view

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
class CartItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image']

class CartItemSerializer(serializers.ModelSerializer):
    product=CartItemProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item:CartItem):
        return cart_item.product.price * cart_item.quantity
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


class OrderItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1, read_only=False)

    class Meta:
        model = OrderItem
        fields = ['product', 'order',  'quantity']


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['customer',
                  'payment_status', 'placed_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        # ensures password not returned/viewed
        extra_kwargs = {"password": {"write_only": True}}
# implements a emthod to create a new version fo the user

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

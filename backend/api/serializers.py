from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import OrderItem, Product, Customer, Order, Address


class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(
        method_name="calculate_tax")

    def calculate_tax(self, product):
        return product.price * Decimal(1.1)

    class Meta:
        model = Product
        fields = ['id', 'name',
                  'description', 'color', 'price', 'image', 'price_with_tax']


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

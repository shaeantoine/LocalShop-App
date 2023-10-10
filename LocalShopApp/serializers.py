from rest_framework import serializers
from .models import User, Product, Order, OrderItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'image')

class OrderSerializer(serializers.ModelSerializer):
    #items = OrderItemSerializer(many=True)
    items = serializers.StringRelatedField(many=True)  # Use StringRelatedField for items


    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'created_at', 'items')

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    order = OrderSerializer() 

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'order', 'quantity')

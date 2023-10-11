# from rest_framework import viewsets
# from rest_framework.response import Response
# from .models import User, Product, Order, OrderItem
# from .serializers import UserSerializer, ProductSerializer, OrderSerializer, OrderItemSerializer
from django.shortcuts import render
from .models import * 

## Depreciated

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def list(self, request):
#         queryset = User.objects.all()
#         serializer = UserSerializer(queryset, many=True)
#         return Response(serializer.data)

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def list(self, request):
#         queryset = Product.objects.all()
#         serializer = ProductSerializer(queryset, many=True)
#         return Response(serializer.data)

# class OrderItemViewSet(viewsets.ModelViewSet):
#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemSerializer

#     def list(self, request):
#         queryset = OrderItem.objects.all()
#         serializer = OrderItemSerializer(queryset, many=True)
#         return Response(serializer.data)

# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

#     def list(self, request):
#         queryset = Order.objects.all()
#         serializer = OrderSerializer(queryset, many=True)
#         return Response(serializer.data)

def localshop(request):
     products = Product.objects.all()
     context = {'products':products}
     return render(request, 'LocalShopApp/localshop.html', context)

def cart(request):
     context = {}
     return render(request, 'LocalShopApp/cart.html', context)

def checkout(request):
      context = {}
      return render(request, 'LocalShopApp/checkout.html', context)
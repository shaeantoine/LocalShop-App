# from rest_framework import viewsets
# from rest_framework.response import Response
# from .models import User, Product, Order, OrderItem
# from .serializers import UserSerializer, ProductSerializer, OrderSerializer, OrderItemSerializer
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .models import * 
from . utils import cookieCart, cartData, guestOrder
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

@csrf_exempt
def localshop(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    query = request.GET.get('q')
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Apply search query, category, and price range filters
    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query)) #| Q(description__icontains=query)

    if category:
        products = products.filter(category=category)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'LocalShopApp/localshop.html', context)


# def localshop(request):
# 	data = cartData(request)
# 	cartItems = data['cartItems']
# 	order = data['order']
# 	items = data['items']

# 	products = Product.objects.all()
# 	context = {'products':products, 'cartItems':cartItems}
# 	return render(request, 'LocalShopApp/localshop.html', context)


def cart(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'LocalShopApp/cart.html', context)


def checkout(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'LocalShopApp/checkout.html', context)



def updateItem(request):
  data = json.loads(request.body) ### changes made here
  productId = data['productId']
  action = data['action']

  print('productId', productId)
  print('Action;', action)

  customer = request.user.customer
  product = Product.objects.get(id=productId)
  order, created = Order.objects.get_or_create(customer=customer, complete=False)
  orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

  if action == 'add':
    orderItem.quantity = (orderItem.quantity + 1)
  elif action == 'remove':
    orderItem.quantity = (orderItem.quantity - 1)
  
  orderItem.save()

  if orderItem.quantity <= 0:
    orderItem.delete()

  return JsonResponse('Item was added', safe=False)


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		#order = Order.objects.create(customer=customer, complete=False, transaction_id=transaction_id)
	else:
		customer, order = guestOrder(request, data)

	# if request.user.is_authenticated:
	# 	customer = request.user.customer
	# else:
	# 	customer, _ = guestOrder(request, data)

    # # Create a new order for the customer each time
	# order = Order.objects.create(customer=customer, complete=False, transaction_id=transaction_id)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)


# def order_history(request):
# 	orders = Order.objects.all()
# 	order_items = OrderItem.objects.filter(order__in=orders)
# 	context = {'orders': orders, 'order_items': order_items}
# 	return render(request, 'LocalShopApp/orderhistory.html', context)

@login_required
def order_history(request):
    if request.user.is_staff:  # Check if the user is an admin
        orders = Order.objects.all()  # Show all orders for admins
        order_items = OrderItem.objects.filter(order__in=orders)
    else:
        customer = request.user.customer  # Get the customer associated with the logged-in user
        orders = Order.objects.filter(customer=customer) 
        order_items = OrderItem.objects.filter(order__in=orders)

    context = {'orders': orders, 'order_items': order_items}
    return render(request, 'LocalShopApp/order_history.html', context)


from django.contrib import messages

def user_login(request):
    error_message = None
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in.')
            return redirect('localshop')  # Redirect to the main page after successful login
        else:
            error_message = "Invalid username or password. Please try again."
            messages.error(request, error_message)
    
    return render(request, 'LocalShopApp/login.html', {'title': 'Login', 'error_message': error_message})


from .forms import RegistrationForm

def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'LocalShopApp/register.html', {'title': 'Register', 'form': form})

def user_logout(request):
    logout(request)
    return redirect('localshop')  # Redirect to the main page after logout
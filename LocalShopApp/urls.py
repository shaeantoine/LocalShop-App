from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.localshop, name="localshop"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
    path('orders/', views.order_history, name='order_history'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),

]
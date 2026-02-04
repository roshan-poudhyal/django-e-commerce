from django.urls import path
from . import views

urlpatterns = [
    # Home and Products
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Cart
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    
    # Orders
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:pk>/', views.order_confirmation, name='order_confirmation'),
    path('orders/', views.orders, name='orders'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
]

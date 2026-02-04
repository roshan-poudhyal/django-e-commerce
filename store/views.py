from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from .models import Product, Category, Cart, CartItem, Order, OrderItem
import json


# Public Views
def home(request):
    products = Product.objects.all()[:6]
    categories = Category.objects.all()
    return render(request, 'store/home.html', {'products': products, 'categories': categories})


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Search
    search = request.GET.get('search')
    if search:
        products = products.filter(Q(name__icontains=search) | Q(description__icontains=search))
    
    # Sort
    sort = request.GET.get('sort', '-created_at')
    products = products.order_by(sort)
    
    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })


# Authentication Views
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            return render(request, 'store/register.html', {'error': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'store/register.html', {'error': 'Username already exists'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        Cart.objects.create(user=user)
        
        user = authenticate(request, username=username, password=password)
        login(request, user)
        return redirect('home')
    
    return render(request, 'store/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'store/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'store/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


# Cart Views
@login_required(login_url='login')
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'store/cart.html', {'cart': cart})


@login_required(login_url='login')
def add_to_cart(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        quantity = int(request.POST.get('quantity', 1))
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        
        cart_item.save()
        
        return redirect('cart')


@login_required(login_url='login')
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')


@login_required(login_url='login')
def update_cart_item(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    
    return redirect('cart')


# Order Views
@login_required(login_url='login')
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    if not cart.items.exists():
        return redirect('cart')
    
    if request.method == 'POST':
        # Create order
        order = Order.objects.create(user=request.user, total_price=cart.get_total_price())
        
        # Create order items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        
        # Clear cart
        cart.items.all().delete()
        
        return redirect('order_confirmation', pk=order.pk)
    
    return render(request, 'store/checkout.html', {'cart': cart})


@login_required(login_url='login')
def order_confirmation(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'store/order_confirmation.html', {'order': order})


@login_required(login_url='login')
def orders(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/orders.html', {'orders': user_orders})


@login_required(login_url='login')
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})

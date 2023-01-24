from django.shortcuts import render, redirect
from .models import Cart
from products.models import Product

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    context = {}
    return render(request, 'carts/home.html', context)

def cart_update(request):
    product = Product.objects.all().first()
    product_id = product.id
    product_obj = Product.objects.get(id=product_id)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    cart_obj.products.add(product_obj)
    return redirect('cart:home')


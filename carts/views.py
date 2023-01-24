from django.shortcuts import render
from .models import Cart

def cart_home(request):
    cart_obj = Cart.objects.new_or_get(request)
    context = {}
    return render(request, 'carts/home.html', context)

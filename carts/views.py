from django.shortcuts import render
from .models import Cart

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    # products = cart_obj.products.all()
    # # import pdb;
    # # pdb.set_trace()
    # total = 0
    # for item in products:
    #     total += item.price
    # cart_obj.total = total
    # cart_obj.save()
    context = {}
    return render(request, 'carts/home.html', context)

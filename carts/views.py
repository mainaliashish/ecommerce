from django.shortcuts import render

def cart_home(request):
    context = {}
    return render(request, 'carts/home.html', context)

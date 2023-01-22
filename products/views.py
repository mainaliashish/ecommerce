from django.shortcuts import render
from .models import Product
from django.views.generic import ListView


class ProductListView(ListView):
    template_name = 'products/list.html'
    queryset = Product.objects.all()


def product_list_view(request):
    querySet = Product.objects.all()
    context = {
        'querySet' : querySet
    }
    return render(request, 'products/list.html', context)


def product_detail_view(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        'product': product
    }
    return render(request, 'products/detail.html', context)

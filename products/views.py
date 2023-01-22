from django.shortcuts import render, get_object_or_404
from .models import Product
from django.views.generic import ListView
from django.http import Http404


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
    # Method 1
    product = get_object_or_404(Product, id=pk)
    # Method 2
    # querySet = Product.objects.filter(id=pk)
    # if querySet.exists() and querySet.count() == 1:
    #     product = querySet.first()
    # else:
    #     raise Http404("Product doesn't exist.")
    context = {
        'product': product
        }
    return render(request, 'products/detail.html', context)

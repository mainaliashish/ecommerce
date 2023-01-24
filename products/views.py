from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from carts.models import Cart
from .models import Product
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


def product_featured_view(request):
    querySet = Product.objects.get_featured()
    context = {
        'querySet': querySet
    }
    return render(request, 'products/featured.html', context)


def product_detail_view(request, slug):
    # Method 1
    # instance = Product.objects.get_by_id(pk)
    instance = Product.objects.get_by_slug(slug)
    if instance is None:
        raise Http404("Product doesn't exist.")

    # Method 2
    # querySet = Product.objects.filter(id=pk)
    # if querySet.exists() and querySet.count() == 1:
    #     product = querySet.first()
    # else:
    #     raise Http404("Product doesn't exist.")
    context = {
        'product': instance
        }
    return render(request, 'products/detail.html', context)

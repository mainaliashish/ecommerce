from django.shortcuts import render
from products.models import Product

def search_product_list_view(request):
    query = request.GET.get('q', None)
    if query is not None:
        querySet = Product.objects.filter(title__icontains=query)
    else:
        querySet = Product.objects.get_featured()

    context = {
        'object_list': querySet
    }
    return render(request, 'products/list.html', context)

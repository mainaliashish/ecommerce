from django.urls import path
from . import views

# URL patterns for products app
urlpatterns = [
    path('', views.search_product_list_view, name='search-products'),
]

from django.urls import path
from . import views

# URL patterns for products app
urlpatterns = [
    path('', views.ProductListView.as_view(), name='products'),
    path('featured-products/', views.product_featured_view, name='featured-products'),
    path('product/<str:pk>/', views.product_detail_view, name="product"),
]

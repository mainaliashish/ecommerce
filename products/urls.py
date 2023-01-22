from django.urls import path
from . import views

# URL patterns for products app
urlpatterns = [
    path('', views.ProductListView.as_view(), name='products'),
]

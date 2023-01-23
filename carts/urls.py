from django.urls import path
from . import views

# URL patterns for products app
urlpatterns = [
    path('', views.cart_home, name='cart-home'),
]

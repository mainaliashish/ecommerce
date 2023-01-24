from django.urls import path
from . import views

# URL patterns for products app
urlpatterns = [
    path('', views.cart_home, name='home'),
    path('update/', views.cart_update, name='update'),
]

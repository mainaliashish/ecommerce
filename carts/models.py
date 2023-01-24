import uuid
from django.db import models
from django.db.models.signals import pre_save, m2m_changed
from django.contrib.auth.models import User
from products.models import Product

class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id

        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    sub_total = models.DecimalField(max_digits=7, decimal_places=3, default=0.00)
    total = models.DecimalField(max_digits=7, decimal_places=3, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

# Register signal to update total

def pre_save_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for item in products:
            total += item.price
        if instance.sub_total != total:
            instance.sub_total = total
            instance.save()


# Connect to pre_save signals
m2m_changed.connect(pre_save_cart_receiver, sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    instance.total = instance.sub_total

pre_save.connect(pre_save_cart_receiver, sender=Cart)

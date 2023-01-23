from django.db import models
from products.utils import unique_slug_generator
from products.models import Product
from django.db.models.signals import pre_save
import uuid

class Tag(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(null=True, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    products = models.ManyToManyField(Product, blank=True)

    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.title


# Register signal to update slug name
def tags_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


# Connect to pre_save signals
pre_save.connect(tags_pre_save_receiver, sender=Tag)



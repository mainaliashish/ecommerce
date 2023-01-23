from django.db import models
import uuid
import random
import os
import time
from django.db.models.signals import pre_save
from products.utils import unique_slug_generator
from django.urls import reverse
from django.db.models import Q

# Get name and extension of the uploaded file
def get_file_extension(file_path):
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    return name, ext

# Custom upload file path
def upload_image_path(instance, filename):
    name, ext = get_file_extension(filename)
    new_file_name = str(random.randint(1, 99999)) + \
        str(round(time.time() * 1000))
    final_file_name = f"{new_file_name}{ext}"
    return f"products/{final_file_name}"


# Product queryset
class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def featured(self):
        return self.filter(featured=True, is_active=True)

    def search(self, query):
        lookups = Q(title__icontains=query) | Q(
            description__icontains=query) | Q(price__icontains=query)
        return self.filter(lookups).distinct()

# Model manager

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def get_by_slug(self, slug):
        qs = self.get_queryset().filter(slug=slug)
        if qs.count() == 1:
            return qs.first()
        return None

    def get_featured(self):
        qs = self.get_queryset().filter(featured=True)
        if qs.count() > 0:
            return qs
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)

# Product model
class Product(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    slug = models.SlugField(blank=True, null=True, unique=True, editable=False)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        default=0, decimal_places=2, max_digits=20, null=True)
    image = models.ImageField(
        upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    objects = ProductManager()

    def get_absolute_url(self):
        # return f"products/{self.slug}/"
        return reverse("detail", kwargs={'slug': self.slug})

    def __str__(self) -> str:
        return self.title

    def __unicode__(self):
        return self.title


# Register signal to update slug name
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

# Connect to pre_save signals
pre_save.connect(product_pre_save_receiver, sender=Product)

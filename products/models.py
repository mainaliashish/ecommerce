from django.db import models
import uuid
import random
import os, time

def get_file_extension(file_path):
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_file_extension(filename)
    new_file_name = str(random.randint(1,99999)) + str(round(time.time() * 1000))
    final_file_name = f"{new_file_name}{ext}"
    return f"products/{final_file_name}"


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def featured(self):
        return self.filter(featured=True, is_active=True)

# Model manager
class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs =  self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def get_featured(self):
        qs = self.get_queryset().filter(featured=True)
        if qs.count() > 0:
            return qs
        return None


class Product(models.Model):
    title = models.CharField(max_length=250,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=20, null=True)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    objects = ProductManager()

    def __str__(self) -> str:
        return self.title

    def __unicode__(self):
        return self.title

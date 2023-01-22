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

class Product(models.Model):
    title = models.CharField(max_length=250,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=20, null=True)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.title

    def __unicode__(self):
        return self.title

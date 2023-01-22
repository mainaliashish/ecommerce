from django.db import models
import uuid

class Product(models.Model):
    title = models.CharField(max_length=250,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.title

    def __unicode__(self):
        return self.title

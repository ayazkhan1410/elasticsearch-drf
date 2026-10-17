from django.db import models


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    class Meta:
        ordering = ["product_name"]

    def __str__(self):
        return self.product_name

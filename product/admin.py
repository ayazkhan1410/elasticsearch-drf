from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "price")
    search_fields = ("product_name", "description")
    list_filter = ("price",)

from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import \
    (
        Category, ProductType,
        Attribute, AttributeValue,
        Product, ProductVariant
    )
# Register your models here.

admin.site.register([
    ProductType,
    Attribute,
    AttributeValue])

admin.site.register(Category, MPTTModelAdmin)

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    fields = ['sku', 'name', 'price', 'quantity', 'quantity_allocated', 'images']


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductVariantInline,
    ]

admin.site.register(Product, ProductAdmin)
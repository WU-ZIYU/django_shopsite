from django.contrib import admin
from .models import Carts, CartLine

# Register your models here.
class CartLineAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

admin.site.register(CartLine, CartLineAdmin)
admin.site.register(Carts)
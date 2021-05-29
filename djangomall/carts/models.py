from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, ValidationError
from django.contrib.auth import get_user_model
from products.models import ProductVariant
User = get_user_model()
# Create your models here.

class Carts(models.Model):
    '''购物车模型'''
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='cart',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.name


class CartLine(models.Model):
    '''购物车条目模型'''
    cart = models.ForeignKey(
        Carts,
        related_name='lines',
        on_delete=models.CASCADE
    )

    product_variant = models.ForeignKey(
        ProductVariant,
        related_name='+',
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1)])

    unit_price = models.DecimalField(max_digits=16, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self):
        return '{0} {1}({2})'.format(
            self.product_variant.product.name,
            self.product_variant.sku,
            self.quantity
        )

    def get_total(self):
        return self.unit_price * self.quantity

    class Meta:
        # 验证购物车+商品变种的组合唯一性
        # 相同商品变种的条目需要加总，所以使用 unique_together 做唯一性验证
        unique_together = ('cart', 'product_variant')
        ordering = ['-created_at']


    def clean(self):
        # 检查如果购物车条目的数量大于商品变种库存，抛出异常
        if self.quantity > self.product_variant.quantity:
            raise ValidationError(('Ensure this value is less than or equal to %(limit_value)s'),
                                  params={'limit_value': self.product_variant.quantity})


    def save(self, *args, **kwargs):
        # 执行检查，包括 .clean()
        self.full_clean()
        return super().save(*args, **kwargs)


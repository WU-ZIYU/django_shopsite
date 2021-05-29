from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager

# Create your models here.
class Category(MPTTModel, models.Model):
    '''分类'''
    name = models.CharField(max_length=256)
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE
    )
    tree = TreeManager()
    def __str__(self):
        return self.name


class ProductType(models.Model):
    '''商品类型'''
    name = models.CharField(max_length=256)
    def __str__(self):
        return self.name


class Attribute(models.Model):
    '''商品类型的属性，和商品类型一对多'''
    name = models.CharField(max_length=256)
    product_type = models.ForeignKey(
        ProductType,
        related_name='product_attributes',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )


    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    '''商品类型属性的值，和商品类型属性一对多'''
    value = models.CharField(max_length=256)
    attribute = models.ForeignKey(
        Attribute,
        related_name='values',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.value


class Product(models.Model):
    '''商品类型，包含多个商品类型属性的值'''
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )

    product_type = models.ForeignKey(
        ProductType,
        related_name='products',
        on_delete=models.CASCADE
    )

    attribute_value = models.ManyToManyField('AttributeValue')
    name = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=16, decimal_places=2)
    # 图片
    image = models.ImageField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    '''一个商品的多版本的模型'''
    product = models.ForeignKey(
        Product,
        related_name='variants',
        on_delete=models.CASCADE
    )
    sku = models.CharField(primary_key=True, max_length=128)
    name = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=16, decimal_places=2)
    images = models.ImageField()
    # 库存数量
    quantity = models.PositiveIntegerField(default=0)
    quantity_allocated = models.PositiveIntegerField(default=0)

    def __str__(self):
        return ('-').join([self.sku, self.name])

    @property
    def base_price(self):
        '''商品变种的价格，如果为空，取商品的价格'''
        return self.price or self.product.price

    @property
    def product_name(self):
        return self.product.name




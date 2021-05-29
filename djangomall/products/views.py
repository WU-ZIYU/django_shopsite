from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from .models import Category, Product, Attribute
from django.core.paginator import Paginator
from rest_framework.generics import RetrieveAPIView
from .serializers import ProductSerializer
# Create your views here.

def get_category(request, category_id):
    # 根据 category_id 查找分类，如果找不到抛出 404
    category = get_object_or_404(Category, id=category_id)
    # 查找子分类
    categories = category.get_descendants(include_self=True)
    # 查找子分类产品
    products = Product.objects.filter(category__in=categories)
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    ctx = {
        'category:': category,
        'products': products,
    }
    return TemplateResponse(request, 'products/get_category.html', ctx)


def get_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # 查找商品所属的商品类型的所有属性
    attributes = Attribute.objects.filter(product_type=product.product_type)

    ctx = {
        'product': product,
        'attributes': attributes
    }

    return TemplateResponse(request, 'products/get_product.html', ctx)


class ProductAPIView(RetrieveAPIView):
    lookup_field = 'id'
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

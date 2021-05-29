from django.template.response import TemplateResponse
from products.models import ProductVariant
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Carts, CartLine
from .serializers import CartLineSerializer

# Create your views here.
def index(request):
    return TemplateResponse(request, 'carts/index.html')


class CartLineViewSet(viewsets.ModelViewSet):
    #queryset = CartLine.objects.all()
    serializer_class = CartLineSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # 取用户购物车数据集的第一条数据
        cart = Carts.objects.filter(user=self.request.user).first()
        # 筛选后返回
        return CartLine.objects.filter(cart=cart)

    def create(self, request, *args, **kwargs):
        # 根据用户查找或创建购物车
        cart, _ = Carts.objects.get_or_create(user=request.user)
        # 查找商品变种
        product_variant = get_object_or_404(
            ProductVariant, pk=request.data.get('product_variant')
        )
        # 复制 POST 的数据，设置 cart 和 unit_price
        data = request.data.copy()
        data['cart'] = cart.pk
        data['unit_price'] = product_variant.base_price

        # 序列化修改后的数据
        serializer = self.get_serializer(data=data)
        # 执行验证，验证通过抛出异常
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data))
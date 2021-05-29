from django.urls import path, include
from products.views import ProductAPIView
from .views import User_apiview
from rest_framework.routers import DefaultRouter, SimpleRouter
from carts.views import CartLineViewSet


router = DefaultRouter()
router.register(r'', User_apiview)

router_cart = SimpleRouter()
router_cart.register('cartlines', CartLineViewSet, 'cartlines')

urlpatterns = [
    path('products/<id>', ProductAPIView.as_view(), name='productsApi'),
    path('users/', include(router.urls), name='usersApi'),
    path('', include(router_cart.urls), name='cartlinesApi'),
]
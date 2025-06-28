from django.urls import path
from .views import UserCartView, UserOrdersView, CartItemManageView, CheckoutView

urlpatterns = [
    path('cart/', UserCartView.as_view(), name='user-cart'),
    path('cart/items/', CartItemManageView.as_view(), name='cart-item-add'),
    path('cart/items/<int:item_id>/', CartItemManageView.as_view(), name='cart-item-modify-delete'),
    path('orders/', UserOrdersView.as_view(), name='user-orders'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]

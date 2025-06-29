from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .permissions import IsModerator

from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, OrderSerializer, CartItemSerializer

class UserCartView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

class UserOrdersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class CartItemManageView(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

    def post(self, request):
        """
        Aggiunge un prodotto al carrello o incrementa la quantità se già presente.
        """
        cart = self.get_cart()
        serializer = CartItemSerializer(data=request.data)

        if serializer.is_valid():
            product = serializer.validated_data.get('product')
            quantity = serializer.validated_data.get('quantity', 1)

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()

            return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

        print("Errore:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, item_id):
        """
        Modifica la quantità di un prodotto nel carrello.
        """
        cart = self.get_cart()
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, item_id):
        """
        Rimuove un prodotto dal carrello.
        """
        cart = self.get_cart()
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        cart_items = cart.items.all()

        if not cart_items.exists():
            return Response({"detail": "Carrello vuoto"}, status=status.HTTP_400_BAD_REQUEST)

        # Controllo disponibilità e regole business
        for item in cart_items:
            if item.quantity > item.product.stock:
                return Response({
                    "detail": f"Prodotto '{item.product.name}' ha solo {item.product.stock} pezzi disponibili"
                }, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Creo ordine
            order = Order.objects.create(user=user)

            # Creo order items e aggiorno stock prodotti
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )
                # Aggiorno stock prodotto
                item.product.stock -= item.quantity
                item.product.save()

            # Pulisco carrello
            cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DeleteOrderView(APIView):
    permission_classes = [IsAuthenticated, IsModerator]

    def delete(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id)
            order.delete()
            return Response({"detail": "Ordine cancellato con successo."}, status=204)
        except Order.DoesNotExist:
            return Response({"detail": "Ordine non trovato."}, status=404)
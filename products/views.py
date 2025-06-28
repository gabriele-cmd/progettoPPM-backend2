from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Product
from .serializers import ProductSerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]  # Può essere visto anche senza login
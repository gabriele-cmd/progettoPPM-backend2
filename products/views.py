from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Product
from .serializers import ProductSerializer
from django.shortcuts import render

def index_view(request):
    return render(request, 'index.html')

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]  # Può essere visto anche senza login
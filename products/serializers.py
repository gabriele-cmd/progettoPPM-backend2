from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'discount_percentage', 'final_price']

    def get_final_price(self, obj):
        return obj.final_price()

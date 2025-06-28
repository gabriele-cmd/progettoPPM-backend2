from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()
    discount_percentage = models.DecimalField(max_digits=2, decimal_places=0)

    def is_available(self):
        return self.stock > 0

    def final_price(self):
        return self.price * (1 - self.discount_percentage / 100)

    def __str__(self):
        return self.name


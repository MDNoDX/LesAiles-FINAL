from django.db import models
from bot.models.order import Order
from bot.models.product import Product
from bot.models.base import BaseModel

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    
    class Meta:
        db_table = 'order_items'
    
    @property
    def total(self):
        return self.quantity * self.price
    
    def __str__(self):
        return f"{self.product.title} x {self.quantity}"
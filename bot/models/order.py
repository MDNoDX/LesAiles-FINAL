from django.db import models
from bot.models.base import BaseModel
from bot.models.user import TelegramUser
from bot.models.branch import Branch
from bot.models.product import Product

class Order(BaseModel):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('click', 'Click'),
        ('payme', 'Payme'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('accepted', 'Accepted'),
        ('preparing', 'Preparing'),
        ('delivering', 'Delivering'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='orders')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    order_type = models.CharField(max_length=20, choices=[('takeaway', 'Takeaway'), ('delivery', 'Delivery')])
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    delivery_address = models.TextField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.first_name} - {self.total_amount}"

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
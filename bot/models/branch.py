from django.db import models
from bot.models.base import BaseModel, City

class Branch(BaseModel):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='branches')
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    opening_hours = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'branches'
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'
    
    def __str__(self):
        return f"{self.name} - {self.city.name}"
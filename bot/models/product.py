from django.db import models
from django.utils.translation import gettext_lazy as _
from bot.models.base import BaseModel

class Category(BaseModel):
    title = models.CharField(max_length=64, verbose_name=_('title'))
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'category'
        verbose_name = _('category')
        verbose_name_plural = _('categories')

class Product(BaseModel):
    title = models.CharField(max_length=64, verbose_name=_('title'))
    price = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField()
    status = models.BooleanField(default=True)
    file_id = models.CharField(max_length=255, blank=True)
    caption = models.TextField(null=True, blank=True)
    temp_file = models.ImageField(upload_to='temp/', null=True, blank=True, verbose_name=_('temp_file'))
    telegram_post_id = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name=_('category'))
    
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'product'
        verbose_name = _('product')
        verbose_name_plural = _('products')
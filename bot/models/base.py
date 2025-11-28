from django.db import models
from django.utils.translation import gettext_lazy as _

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class City(BaseModel):
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'city'
        verbose_name = _('city')
        verbose_name_plural = _('cities')
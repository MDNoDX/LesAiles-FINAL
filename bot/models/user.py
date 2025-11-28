from django.db import models
from bot.models.base import City

class TelegramUser(models.Model):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('uz', 'O\'zbekcha'),
    ]
    user_id = models.BigIntegerField(unique=True, db_index=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    language_code = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en')
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='users', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'telegram_users'
    def __str__(self):
        return f"{self.user_id} - {self.first_name or 'No name'}"
from django.urls import path

from . import views

app_name = 'bot'

urlpatterns = [
    path('webhook/', views.webhook, name='webhook'),
    path('set-webhook/', views.set_webhook_view, name='set_webhook'),
    path('webhook-info/', views.webhook_info_view, name='webhook_info'),
    path('health/', views.health_check, name='health'),
]
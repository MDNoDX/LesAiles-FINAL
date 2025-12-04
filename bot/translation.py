from asgiref.sync import sync_to_async
from django.conf import settings
from bot.models.user import TelegramUser

@sync_to_async
def get_user_language(user_id):
    try:
        user = TelegramUser.objects.get(user_id=user_id)
        return user.language_code
    except TelegramUser.DoesNotExist:
        return settings.LANGUAGE_CODE

@sync_to_async
def set_user_language(user_id, language_code):
    user, created = TelegramUser.objects.get_or_create(
        user_id=user_id,
        defaults={'language_code': language_code}
    )
    if not created:
        user.language_code = language_code
        user.save(update_fields=['language_code'])

@sync_to_async
def get_or_create_user(user_id, username=None, first_name=None, last_name=None):
    user, created = TelegramUser.objects.get_or_create(
        user_id=user_id,
        defaults={
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'language_code': 'en'
        }
    )
    if not created:
        update_fields = []
        if username and user.username != username:
            user.username = username
            update_fields.append('username')
        if first_name and user.first_name != first_name:
            user.first_name = first_name
            update_fields.append('first_name')
        if last_name and user.last_name != last_name:
            user.last_name = last_name
            update_fields.append('last_name')
        if update_fields:
            user.save(update_fields=update_fields)
    return user, created
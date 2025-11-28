import json
import logging
from aiogram.types import Update
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from bot.apps import BotConfig

logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
async def webhook(request):
    try:
        update_data = json.loads(request.body.decode('utf-8'))
        update = Update(**update_data)
        await BotConfig.dp.feed_update(bot=BotConfig.bot, update=update)
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        logger.error(f"Webhook error: {e}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

async def set_webhook_view(request):
    from core import config
    try:
        webhook_url = f"{config.BASE_WEBHOOK_URL}{config.WEBHOOK_PATH}"
        await BotConfig.bot.set_webhook(
            url=webhook_url,
            secret_token=config.WEBHOOK_SECRET,
            drop_pending_updates=True
        )
        webhook_info = await BotConfig.bot.get_webhook_info()
        return JsonResponse({
            'status': 'success',
            'message': f'Webhook set to: {webhook_url}',
            'webhook_info': {
                'url': webhook_info.url,
                'pending_update_count': webhook_info.pending_update_count
            }
        })
    except Exception as e:
        logger.error(f"Set webhook error: {e}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

async def webhook_info_view(request):
    try:
        webhook_info = await BotConfig.bot.get_webhook_info()
        return JsonResponse({
            'status': 'success',
            'webhook_info': {
                'url': webhook_info.url,
                'has_custom_certificate': webhook_info.has_custom_certificate,
                'pending_update_count': webhook_info.pending_update_count,
                'last_error_date': webhook_info.last_error_date,
                'last_error_message': webhook_info.last_error_message,
                'max_connections': webhook_info.max_connections,
            }
        })
    except Exception as e:
        logger.error(f"Webhook info error: {e}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def health_check(request):
    return JsonResponse({'status': 'ok'})
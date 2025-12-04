import json
import logging
import asyncio
from aiogram.types import Update
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from bot.apps import BotConfig

logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
async def webhook(request):
    try:
        update_data = json.loads(request.body.decode('utf-8'))
        update = Update(**update_data)
        
        bot = await BotConfig.get_bot()
        dp = await BotConfig.get_dp()
        
        await dp.feed_update(bot=bot, update=update)
        return JsonResponse({'status': 'ok'})
        
    except Exception as e:
        logger.error(f"Webhook error: {e}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_GET
async def set_webhook_view(request):
    try:
        from core import config
        
        bot = await BotConfig.get_bot()
        
        webhook_url = f"{config.BASE_WEBHOOK_URL}{config.WEBHOOK_PATH}"
        
        logger.info(f"Setting webhook to: {webhook_url}")
        
        await bot.set_webhook(
            url=webhook_url,
            secret_token=config.WEBHOOK_SECRET,
            drop_pending_updates=True
        )
        
        webhook_info = await bot.get_webhook_info()
        
        return JsonResponse({
            'status': 'success',
            'message': f'✅ Webhook set successfully!',
            'webhook_url': webhook_url,
            'webhook_info': {
                'url': webhook_info.url,
                'pending_update_count': webhook_info.pending_update_count,
                'max_connections': webhook_info.max_connections,
            }
        })
        
    except Exception as e:
        logger.error(f"Set webhook error: {e}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_GET
async def webhook_info_view(request):
    try:
        bot = await BotConfig.get_bot()
        webhook_info = await bot.get_webhook_info()
        
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

@require_GET
async def delete_webhook_view(request):
    try:
        bot = await BotConfig.get_bot()
        
        result = await bot.delete_webhook(drop_pending_updates=True)
        
        return JsonResponse({
            'status': 'success',
            'message': '✅ Webhook deleted successfully!',
            'result': result
        })
        
    except Exception as e:
        logger.error(f"Delete webhook error: {e}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_GET
async def health_check(request):
    return JsonResponse({'status': 'ok', 'bot_initialized': BotConfig._initialized})
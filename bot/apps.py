import logging
from aiogram import Bot, Dispatcher
from django.apps import AppConfig
from core import config

logger = logging.getLogger(__name__)

class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'

    bot: Bot = None
    dp: Dispatcher = None

    def ready(self):
        if not BotConfig.bot:
            logger.info("Initializing bot...")

            BotConfig.bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
            BotConfig.dp = Dispatcher()

            try:
                from bot.middlewares.i18n import TranslationMiddleware
                BotConfig.dp.message.middleware(TranslationMiddleware())
                BotConfig.dp.callback_query.middleware(TranslationMiddleware())

                from bot.handlers.start import router as start_router
                from bot.handlers.menu import router as menu_router
                from bot.handlers.backs import router as backs_router
                from bot.handlers.order import router as order_router
                from bot.handlers.catalog import router as catalog_router
                from bot.handlers.cart import router as cart_router

                BotConfig.dp.include_router(start_router)
                BotConfig.dp.include_router(menu_router)
                BotConfig.dp.include_router(backs_router)
                BotConfig.dp.include_router(order_router)
                BotConfig.dp.include_router(catalog_router)
                BotConfig.dp.include_router(cart_router)

                logger.info("Bot initialized successfully with i18n support")
            except Exception as e:
                logger.error(f"Error initializing bot: {e}")
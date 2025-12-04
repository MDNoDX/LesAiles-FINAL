import logging
import asyncio
from django.apps import AppConfig

logger = logging.getLogger(__name__)

class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'
    
    _bot_instance = None
    _dp_instance = None
    _initialized = False
    _lock = asyncio.Lock()

    @classmethod
    async def get_bot(cls):
        async with cls._lock:
            if cls._bot_instance is None:
                await cls._initialize()
            return cls._bot_instance

    @classmethod
    async def get_dp(cls):
        async with cls._lock:
            if cls._dp_instance is None:
                await cls._initialize()
            return cls._dp_instance

    @classmethod
    async def _initialize(cls):
        if cls._initialized:
            return
            
        try:
            from aiogram import Bot, Dispatcher
            from aiogram.fsm.storage.memory import MemoryStorage
            from core import config
            
            logger.info("🚀 Initializing Aiogram bot...")
            
            cls._bot_instance = Bot(token=config.TELEGRAM_BOT_TOKEN)
            cls._dp_instance = Dispatcher(storage=MemoryStorage())
            
            from bot.middlewares.i18n import TranslationMiddleware
            cls._dp_instance.message.middleware(TranslationMiddleware())
            cls._dp_instance.callback_query.middleware(TranslationMiddleware())
            
            from bot.handlers.start import router as start_router
            from bot.handlers.menu import router as menu_router
            from bot.handlers.backs import router as backs_router
            from bot.handlers.order import router as order_router
            from bot.handlers.catalog import router as catalog_router
            from bot.handlers.cart import router as cart_router
            from bot.handlers.settings import router as settings_router
            from bot.handlers.order_complete import router as order_complete_router
            from bot.handlers.info import router as info_router
            from bot.handlers.history import router as history_router
                        
            cls._dp_instance.include_router(start_router)
            cls._dp_instance.include_router(menu_router)
            cls._dp_instance.include_router(backs_router)
            cls._dp_instance.include_router(order_router)
            cls._dp_instance.include_router(catalog_router)
            cls._dp_instance.include_router(cart_router)
            cls._dp_instance.include_router(settings_router)
            cls._dp_instance.include_router(order_complete_router)
            cls._dp_instance.include_router(info_router)
            cls._dp_instance.include_router(history_router)
            
            cls._initialized = True
            logger.info("✅ Bot initialized successfully!")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize bot: {e}")
            raise
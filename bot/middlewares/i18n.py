from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from django.utils.translation import activate
from bot.utils.translation import get_user_language

class TranslationMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        language = await get_user_language(user_id)
        activate(language)
        data['user_language'] = language
        return await handler(event, data)
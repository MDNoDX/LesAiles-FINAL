from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from django.utils.translation import gettext as _

async def get_user_main_keyboards():
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=_("🛍 Make an order")),
            ],
            [
                KeyboardButton(text=_("📊 Order history")),
            ],
            [
                KeyboardButton(text=_("⚙️ Settings")),
                KeyboardButton(text=_("ℹ️ Information")),
            ],
            [
                KeyboardButton(text=_("🔥 Promotions")),
            ],
            [
                KeyboardButton(text=_("👥 Join our team")),
                KeyboardButton(text=_("🏢 Contact Les Ailes")),
            ],
        ]
    )
    return keyboard

async def get_settings_keyboards():
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=_("🌐 Change language")),
            ],
            [
                KeyboardButton(text=_("🏙️ Change city")),
            ],
            [
                KeyboardButton(text=_("⬅️ Back")),
            ]
        ]
    )
    return keyboard
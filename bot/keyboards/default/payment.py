from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from django.utils.translation import gettext as _

async def get_payment_keyboards():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="💵 " + _("Cash")),
                KeyboardButton(text="💳 " + _("Card")),
            ],
            [
                KeyboardButton(text="📱 " + _("Click")),
                KeyboardButton(text="📲 " + _("Payme")),
            ],
            [
                KeyboardButton(text="⬅️ " + _("Back")),
            ]
        ]
    )
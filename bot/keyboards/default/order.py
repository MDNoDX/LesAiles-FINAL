from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from django.utils.translation import gettext as _

async def get_order_type_keyboards():
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="🏃‍♂️" + _(" Take away")),
                KeyboardButton(text="🚛 " + _("Delivery")),
            ],
            [
                KeyboardButton(text="⬅️ " + _("Back")),
            ]
        ]
    )
    return keyboard

async def get_takeaway_keyboards():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="⬅️ " + _("Back")),
            ],
            [
                KeyboardButton(text="📍 " + _("Determine nearest branch"), request_location=True),
            ],
            [
                KeyboardButton(text="🌐 " + _("Order here")),
                KeyboardButton(text=_("Select branch")),
            ]
        ]
    )
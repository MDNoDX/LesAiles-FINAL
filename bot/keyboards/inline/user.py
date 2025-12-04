from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.utils.translation import gettext as _

async def get_language_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en"),
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
        ]
    ])
    return keyboard

async def get_categories_keyboard(categories):
    keyboard = []
    for category in categories:
        keyboard.append([InlineKeyboardButton(
            text=category.title, 
            callback_data=f"category_{category.id}"
        )])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def get_products_keyboard(products):
    keyboard = []
    for product in products:
        keyboard.append([InlineKeyboardButton(
            text=f"{product.title} - {product.price} so'm", 
            callback_data=f"product_{product.id}"
        )])
    keyboard.append([InlineKeyboardButton(text="⬅️ " + _("Back"), callback_data="back_to_categories")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def get_quantity_keyboard(product_id, current_quantity=1):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➖", callback_data=f"decrease_{product_id}"),
            InlineKeyboardButton(text=str(current_quantity), callback_data=f"show_{product_id}"),
            InlineKeyboardButton(text="➕", callback_data=f"increase_{product_id}"),
        ],
        [
            InlineKeyboardButton(text="📥 " + _("Add to cart"), callback_data=f"add_{product_id}_{current_quantity}"),
        ],
        [
            InlineKeyboardButton(text="⬅️ " + _("Back"), callback_data="back_to_products"),
        ]
    ])
    return keyboard
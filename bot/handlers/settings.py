from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from django.utils.translation import gettext as _
from bot.keyboards.default.user import get_user_main_keyboards, get_settings_keyboards
from bot.keyboards.inline.user import get_language_keyboard
from bot.utils.translation import set_user_language

router = Router()

@router.message(F.text.in_(['⚙️ Settings', '⚙️ Sozlamalar', '⚙️ Настройки']))
async def settings_handler(message: Message):
    text = _("Settings")
    await message.answer(text=text, reply_markup=await get_settings_keyboards())

@router.message(F.text.in_(['🌐 Change language', '🌐 Tilni o\'zgartirish', '🌐 Изменить язык']))
async def change_language_handler(message: Message):
    text = _("Choose your language:")
    await message.answer(text=text, reply_markup=await get_language_keyboard())

@router.callback_query(F.data.startswith("lang_"))
async def set_language_handler(call: CallbackQuery):
    language_code = call.data.split("_")[1]
    user_id = call.from_user.id
    
    await set_user_language(user_id, language_code)
    
    await call.answer(_("Language changed successfully!"), show_alert=True)
    
    from django.utils.translation import activate
    activate(language_code)
    
    text = _("Settings")
    await call.message.answer(text=text, reply_markup=await get_settings_keyboards())

@router.message(F.text.in_(['⬅️ Back', '⬅️ Ortga', '⬅️ Назад']))
async def back_from_settings(message: Message):
    text = _('Welcome to main menu 😊')
    await message.answer(text=text, reply_markup=await get_user_main_keyboards())
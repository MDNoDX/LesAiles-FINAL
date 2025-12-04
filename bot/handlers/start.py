from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from django.utils.translation import gettext as _
from bot.keyboards.builder import default_keyboard_builder
from bot.keyboards.default.user import get_user_main_keyboards
from bot.keyboards.inline.user import get_language_keyboard
from bot.states.auth import RegisterState
from bot.utils.city import get_all_cities, get_city
from bot.utils.translation import set_user_language, get_or_create_user
from bot.utils.user import partial_update_user

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(RegisterState.language)
    user = message.from_user

    user, created = await get_or_create_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    if created:
        welcome_text = """Assalomu alaykum! Les Ailes yetkazib berish xizmatiga xush kelibsiz.

Здравствуйте! Добро пожаловать в службу доставки Les Ailes.

Hello! Welcome to Les Ailes delivery service."""
        await message.answer(
            welcome_text,
            reply_markup=await get_language_keyboard()
        )
    else:
        cities = await get_all_cities()
        text = _("Please select the city")
        await message.answer(
            text,
            reply_markup=await default_keyboard_builder(
                message=message, keyboards=cities, column_name='name'
            )
        )
        await state.set_state(RegisterState.city)

@router.callback_query(F.data.startswith("lang_"), RegisterState.language)
async def change_language(call: CallbackQuery, state: FSMContext):
    language_code = call.data.split("_")[1]
    user_id = call.from_user.id

    await set_user_language(user_id, language_code)

    try:
        await call.message.delete()
    except:
        pass

    cities = await get_all_cities()
    text = _("Please choose the city")
    await call.message.answer(
        text,
        reply_markup=await default_keyboard_builder(
            message=call.message, keyboards=cities, column_name='name'
        )
    )

    await state.set_state(RegisterState.city)

@router.message(RegisterState.city)
async def get_city_handler(message: Message, state: FSMContext):
    city = await get_city(city_name=message.text)
    
    if city:
        await partial_update_user(data={'city_id': city.id}, user_id=message.chat.id)
        text = _('Welcome to main menu 😊')
        await message.answer(text=text, reply_markup=await get_user_main_keyboards())
        await state.clear()
    else:
        text = _("City not found. Please select from the list:")
        cities = await get_all_cities()
        await message.answer(
            text,
            reply_markup=await default_keyboard_builder(
                message=message, keyboards=cities, column_name='name'
            )
        )
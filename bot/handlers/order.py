from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from django.utils.translation import gettext as _

from bot.keyboards.default.order import get_takeaway_keyboards
from bot.states.order import OrderState

router = Router()

@router.message(F.text.in_(['🏃‍♂️ Take away', '🏃‍♂️ Olib kelish']), OrderState.order_type)
async def take_away_handler(message: Message, state: FSMContext):
    await state.update_data(order_type='take_away')
    await state.set_state(OrderState.location)
    text = _("Where are you? Send your location and we determine the nearest branch to you")
    await message.answer(text=text, reply_markup=await get_takeaway_keyboards())

@router.message(F.text.in_(['📍 Determine nearest branch', '📍 Manzilni ulashish']), OrderState.location)
async def location_button_handler(message: Message, state: FSMContext):
    text = _("Please send your location using the button below")
    await message.answer(text=text)

@router.message(F.location, OrderState.location)
async def location_received_handler(message: Message, state: FSMContext):
    await state.update_data(
        longitude=message.location.longitude,
        latitude=message.location.latitude
    )
    await state.set_state(OrderState.category)
    
    text = _("Where to start?")
    await message.answer(text=text)
    
    from bot.keyboards.inline.user import get_categories_keyboard
    from bot.utils.product import get_categories
    
    categories = await get_categories()
    if categories:
        await message.answer(
            _("Please choose a category:"),
            reply_markup=await get_categories_keyboard(categories)
        )
    else:
        await message.answer(_("No categories available at the moment"))
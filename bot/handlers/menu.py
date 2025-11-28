from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from django.utils.translation import gettext as _

from bot.keyboards.default.order import get_order_type_keyboards
from bot.states.order import OrderState

router = Router()

@router.message(F.text.in_(['🛍 Make an order', '🛍 Buyurtma berish']))
async def make_order_handler(message: Message, state: FSMContext):
    await state.set_state(OrderState.order_type)
    text = _("Take away  🙋‍♂️ or delivery 🚙")
    await message.answer(text=text, reply_markup=await get_order_type_keyboards())
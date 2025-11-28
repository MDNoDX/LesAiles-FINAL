from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from django.utils.translation import gettext as _

from bot.keyboards.inline.user import get_categories_keyboard
from bot.states.order import OrderState
from bot.utils.product import get_categories

router = Router()

@router.callback_query(F.data == "continue_shopping", OrderState.cart)
async def continue_shopping(call: CallbackQuery, state: FSMContext):
    categories = await get_categories()
    if categories:
        await call.message.edit_text(
            _("Please choose a category:"),
            reply_markup=await get_categories_keyboard(categories)
        )
        await state.set_state(OrderState.category)
    else:
        await call.answer(_("No categories available"), show_alert=True)

@router.callback_query(F.data == "complete_order", OrderState.cart)
async def complete_order(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cart = data.get('cart', [])
    
    if not cart:
        await call.answer(_("Your cart is empty"), show_alert=True)
        return

    total = sum(item['total'] for item in cart)

    order_text = _("📋 **Order Summary**\n\n")
    for i, item in enumerate(cart, 1):
        order_text += f"{i}. {item['title']}\n{item['quantity']} x {item['price']:,.0f} = {item['total']:,.0f} so'm\n\n"
    
    order_text += _("**Total: {total:,.0f} so'm**\n\n").format(total=total)
    order_text += _("✅ Your order has been accepted! We will contact you shortly.")
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    order_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=_("🔄 New Order"), callback_data="new_order"),
            InlineKeyboardButton(text=_("🏠 Main Menu"), callback_data="main_menu"),
        ]
    ])
    
    await call.message.answer(order_text, reply_markup=order_keyboard)
    
    await state.clear()

@router.callback_query(F.data == "clear_cart", OrderState.cart)
async def clear_cart(call: CallbackQuery, state: FSMContext):
    await state.update_data(cart=[])
    await call.answer(_("Cart cleared"), show_alert=True)
    
    categories = await get_categories()
    if categories:
        await call.message.edit_text(
            _("Cart cleared. Please choose a category:"),
            reply_markup=await get_categories_keyboard(categories)
        )
        await state.set_state(OrderState.category)

@router.callback_query(F.data == "new_order")
async def new_order(call: CallbackQuery, state: FSMContext):
    categories = await get_categories()
    if categories:
        await call.message.edit_text(
            _("Please choose a category:"),
            reply_markup=await get_categories_keyboard(categories)
        )
        await state.set_state(OrderState.category)
    else:
        await call.answer(_("No categories available"), show_alert=True)

@router.callback_query(F.data == "main_menu")
async def main_menu(call: CallbackQuery, state: FSMContext):
    from bot.keyboards.default.user import get_user_main_keyboards
    await state.clear()
    await call.message.answer(
        _('Welcome to main menu 😊'),
        reply_markup=await get_user_main_keyboards()
    )
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from django.utils.translation import gettext as _
from bot.states.order import OrderState
from bot.keyboards.default.payment import get_payment_keyboards
from bot.utils.branch import get_nearest_branch
from bot.utils.order import create_order
from bot.keyboards.default.user import get_user_main_keyboards

router = Router()

@router.message(OrderState.cart)
async def process_cart_to_checkout(message: Message, state: FSMContext):
    data = await state.get_data()
    cart = data.get('cart', [])
    
    if not cart:
        await message.answer(_("Your cart is empty"))
        return
    
    await state.set_state(OrderState.payment)
    text = _("Choose payment method:")
    await message.answer(text=text, reply_markup=await get_payment_keyboards())

@router.message(F.text.in_(
    ['💵 Cash', '💵 Naqd', '💵 Наличные',
     '💳 Card', '💳 Karta', '💳 Карта',
     '📱 Click', '📱 Клик',
     '📲 Payme', '📲 Пэйми']), OrderState.payment)
async def payment_method_handler(message: Message, state: FSMContext):
    payment_text = message.text
    if 'Cash' in payment_text or 'Naqd' in payment_text or 'Наличные' in payment_text:
        payment_method = 'cash'
    elif 'Card' in payment_text or 'Karta' in payment_text or 'Карта' in payment_text:
        payment_method = 'card'
    elif 'Click' in payment_text or 'Клик' in payment_text:
        payment_method = 'click'
    elif 'Payme' in payment_text or 'Пэйми' in payment_text:
        payment_method = 'payme'
    else:
        payment_method = 'cash'
    
    await state.update_data(payment_method=payment_method)
    
    data = await state.get_data()
    user_lat = data.get('latitude')
    user_lon = data.get('longitude')
    city_id = data.get('city_id')
    
    if user_lat and user_lon:
        nearest_branch, distance = await get_nearest_branch(user_lat, user_lon, city_id)
        if nearest_branch:
            await state.update_data(branch_id=nearest_branch.id)
            branch_info = _(
                "📍 Nearest branch: {name}\n"
                "🏠 Address: {address}\n"
                "📞 Phone: {phone}\n"
                "⏰ Working hours: {hours}"
            ).format(
                name=nearest_branch.name,
                address=nearest_branch.address,
                phone=nearest_branch.phone,
                hours=nearest_branch.opening_hours
            )
            await message.answer(branch_info)
    
    await state.set_state(OrderState.contact)
    text = _("Please send your contact phone number:")
    await message.answer(text=text)

@router.message(OrderState.contact)
async def contact_received_handler(message: Message, state: FSMContext):
    contact_phone = message.text
    if not contact_phone.replace('+', '').isdigit() or len(contact_phone.replace('+', '')) < 9:
        await message.answer(_("Please enter a valid phone number"))
        return
    
    await state.update_data(contact_phone=contact_phone)
    
    await state.set_state(OrderState.comment)
    text = _("Any comments for your order? (or type 'skip' to skip)")
    await message.answer(text=text)

@router.message(F.text.lower() == "skip", OrderState.comment)
async def skip_comment_handler(message: Message, state: FSMContext):
    await complete_order_process(message, state)

@router.message(OrderState.comment)
async def comment_received_handler(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await complete_order_process(message, state)

async def complete_order_process(message: Message, state: FSMContext):
    data = await state.get_data()
    
    order = await create_order(
        user_id=message.from_user.id,
        order_data=data
    )
    
    if order:
        total = sum(item['total'] for item in data.get('cart', []))
        
        order_text = _("🎉 **Order Confirmed!** 🎉\n\n")
        order_text += _("📋 **Order #{order_id}**\n").format(order_id=order.id)
        order_text += _("📅 Date: {date}\n").format(date=order.created_at.strftime("%Y-%m-%d %H:%M"))
        order_text += _("💰 Total: {total:,.0f} so'm\n").format(total=total)
        
        payment_methods = {
            'cash': _('Cash'),
            'card': _('Card'),
            'click': _('Click'),
            'payme': _('Payme')
        }
        payment_text = payment_methods.get(data.get('payment_method', 'cash'), _('Cash'))
        order_text += _("💳 Payment: {method}\n").format(method=payment_text)
        order_text += _("📞 Contact: {phone}\n\n").format(phone=data.get('contact_phone', ''))
        
        order_text += _("📦 **Items:**\n")
        for i, item in enumerate(data.get('cart', []), 1):
            order_text += f"{i}. {item['title']}\n"
            order_text += _("   {quantity} x {price:,.0f} = {total:,.0f} so'm\n").format(
                quantity=item['quantity'],
                price=item['price'],
                total=item['total']
            )
        
        order_text += _("\n✅ Your order has been accepted!\n")
        order_text += _("⏰ We will contact you shortly.\n")
        order_text += _("📞 For questions: +998 90 123 45 67")
        
        await message.answer(order_text, reply_markup=await get_user_main_keyboards())
        
        await state.clear()
        
        await notify_admin_about_order(order)
    else:
        await message.answer(_("❌ Error creating order. Please try again."))

async def notify_admin_about_order(order):
    try:
        from core import config
        admin_text = f"🆕 New Order #{order.id}\n"
        admin_text += f"👤 User: {order.user.first_name} (@{order.user.username})\n"
        admin_text += f"💰 Amount: {order.total_amount:,.0f} so'm\n"
        admin_text += f"📱 Phone: {order.contact_phone}\n"
        
        from bot.apps import BotConfig
        await BotConfig.bot.send_message(
            chat_id=config.TELEGRAM_STORAGE_CHAT_ID,
            text=admin_text
        )
    except:
        pass
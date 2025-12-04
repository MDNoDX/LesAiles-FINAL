from aiogram import Router, F
from aiogram.types import Message
from django.utils.translation import gettext as _
from bot.utils.order import get_user_orders

router = Router()

@router.message(F.text.in_(['📊 Order history', '📊 Buyurtmalar tarixi', '📊 История заказов']))
async def order_history_handler(message: Message):
    user_id = message.from_user.id
    orders = await get_user_orders(user_id, limit=5)
    
    if not orders:
        text = _("You have no orders yet. Make your first order! 🛍")
        await message.answer(text)
        return
    
    text = _("📊 **Your Last Orders:**\n\n")
    
    for order in orders:
        status_icons = {
            'new': '🆕',
            'accepted': '✅',
            'preparing': '👨‍🍳',
            'delivering': '🚚',
            'completed': '🎉',
            'cancelled': '❌'
        }
        
        payment_methods = {
            'cash': _('Cash'),
            'card': _('Card'),
            'click': _('Click'),
            'payme': _('Payme')
        }
        
        status_icon = status_icons.get(order.status, '📝')
        payment_text = payment_methods.get(order.payment_method, _('Cash'))
        
        text += f"{status_icon} **Order #{order.id}**\n"
        text += f"📅 {order.created_at.strftime('%d.%m.%Y %H:%M')}\n"
        text += f"💰 {order.total_amount:,.0f} so'm\n"
        text += f"💳 {payment_text}\n"
        text += f"📦 {order.get_status_display()}\n"
        
        if order.branch:
            text += f"📍 {order.branch.name}\n"
        
        text += "\n" + "─" * 20 + "\n\n"
    
    text += _("📞 For order details: +998 71 200 00 00")
    
    await message.answer(text)
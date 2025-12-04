from aiogram import Router, F
from aiogram.types import Message
from django.utils.translation import gettext as _

router = Router()

@router.message(F.text.in_(['ℹ️ Information', 'ℹ️ Ma\'lumot', 'ℹ️ Информация']))
async def info_handler(message: Message):
    text = _(
        "🏢 **Les Ailes** - Fast Food Restaurant\n\n"
        "📍 **Our branches:**\n"
        "- Tashkent City\n"
        "- Samarkand\n"
        "- Bukhara\n\n"
        "⏰ **Working hours:** 09:00 - 23:00\n"
        "📞 **Phone:** +998 71 200 00 00\n"
        "📧 **Email:** info@lesailes.uz\n\n"
        "🚚 **Delivery:** Available within 60 minutes\n"
        "💳 **Payment methods:** Cash, Card, Click, Payme\n\n"
        "✅ **Quality guarantee!**"
    )
    await message.answer(text)

@router.message(F.text.in_(['🔥 Promotions', '🔥 Aksiyalar', '🔥 Акции']))
async def promotions_handler(message: Message):
    text = _(
        "🔥 **Current Promotions:**\n\n"
        "🎉 **Buy 2 burgers, get 1 free!**\n"
        "Valid until: 31.12.2024\n\n"
        "🎂 **Birthday discount - 20%!**\n"
        "Show your ID on your birthday\n\n"
        "👨‍👩‍👧‍👦 **Family combo - 15% discount**\n"
        "For orders over 150,000 so'm\n\n"
        "📱 **App order - 10% discount**\n"
        "Order through our mobile app\n\n"
        "Stay tuned for more promotions!"
    )
    await message.answer(text)

@router.message(F.text.in_(['👥 Join our team', '👥 Jamoaga qo\'shiling', '👥 Присоединиться к команде']))
async def join_team_handler(message: Message):
    text = _(
        "👥 **Join Les Ailes Team!**\n\n"
        "We are looking for talented people:\n\n"
        "📋 **Vacancies:**\n"
        "- Cook\n"
        "- Delivery driver\n"
        "- Cashier\n"
        "- Manager\n\n"
        "📞 **Contact HR:** +998 71 200 11 11\n"
        "📧 **Send CV:** hr@lesailes.uz\n\n"
        "✅ **Benefits:**\n"
        "- Competitive salary\n"
        "- Flexible schedule\n"
        "- Career growth\n"
        "- Training programs"
    )
    await message.answer(text)

@router.message(F.text.in_(['🏢 Contact Les Ailes', '🏢 Les Ailes bilan bog\'lanish', '🏢 Связаться с Les Ailes']))
async def contact_handler(message: Message):
    text = _(
        "📞 **Contact Us:**\n\n"
        "**Head Office:**\n"
        "📍 Tashkent City, Mustaqillik street\n"
        "📞 +998 71 200 00 00\n"
        "📧 info@lesailes.uz\n\n"
        "**Delivery Service:**\n"
        "📞 +998 71 200 22 22\n"
        "🕒 09:00 - 23:00\n\n"
        "**Customer Support:**\n"
        "📞 +998 71 200 33 33\n"
        "📧 support@lesailes.uz\n\n"
        "**Follow us:**\n"
        "📱 Instagram: @lesailes_uz\n"
        "📱 Facebook: LesAilesUz\n"
        "📱 Telegram: @lesailes_bot"
    )
    await message.answer(text)
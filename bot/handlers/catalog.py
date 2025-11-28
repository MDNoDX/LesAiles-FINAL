from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from django.utils.translation import gettext as _

from bot.keyboards.inline.user import get_products_keyboard, get_quantity_keyboard, get_categories_keyboard
from bot.states.order import OrderState
from bot.utils.product import get_categories, get_products_by_category, get_product_by_id

router = Router()

@router.callback_query(F.data.startswith("category_"), OrderState.category)
async def category_selected(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split("_")[1])
    
    products = await get_products_by_category(category_id)
    if products:
        await call.message.edit_text(
            _("Please choose a product:"),
            reply_markup=await get_products_keyboard(products)
        )
        await state.update_data(category_id=category_id)
        await state.set_state(OrderState.product)
    else:
        await call.answer(_("No products in this category"), show_alert=True)

@router.callback_query(F.data == "back_to_categories", OrderState.product)
async def back_to_categories(call: CallbackQuery, state: FSMContext):
    categories = await get_categories()
    if categories:
        await call.message.edit_text(
            _("Please choose a category:"),
            reply_markup=await get_categories_keyboard(categories)
        )
        await state.set_state(OrderState.category)
    else:
        await call.answer(_("No categories available"), show_alert=True)

@router.callback_query(F.data.startswith("product_"), OrderState.product)
async def product_selected(call: CallbackQuery, state: FSMContext):
    product_id = int(call.data.split("_")[1])
    product = await get_product_by_id(product_id)
    
    if product:
        await state.update_data(
            current_product_id=product.id,
            current_product_title=product.title, 
            current_product_price=float(product.price),
            current_quantity=1
        )
        
        try:
            if product.file_id:
                caption = f"**{product.title}**\n\n{product.description}\n\n**Price: {product.price} so'm**\n\n{_('Select quantity:')}"
                await call.message.answer_photo(
                    photo=product.file_id,
                    caption=caption,
                    reply_markup=await get_quantity_keyboard(product.id, 1)
                )
                await call.message.delete()
            else:
                text = f"**{product.title}**\n\n{product.description}\n\n**Price: {product.price} so'm**\n\n{_('Select quantity:')}"
                await call.message.edit_text(
                    text,
                    reply_markup=await get_quantity_keyboard(product.id, 1)
                )
        except Exception as e:
            text = f"**{product.title}**\n\n{product.description}\n\n**Price: {product.price} so'm**\n\n{_('Select quantity:')}"
            await call.message.edit_text(
                text,
                reply_markup=await get_quantity_keyboard(product.id, 1)
            )
        
        await state.set_state(OrderState.quantity)
    else:
        await call.answer(_("Product not found"), show_alert=True)

@router.callback_query(F.data.startswith("increase_"), OrderState.quantity)
async def increase_quantity(call: CallbackQuery, state: FSMContext):
    product_id = int(call.data.split("_")[1])
    data = await state.get_data()
    
    current_quantity = data.get('current_quantity', 1)
    current_quantity += 1
    
    if current_quantity > 10:
        current_quantity = 10
        await call.answer(_("Maximum quantity is 10"), show_alert=False)
    
    await state.update_data(current_quantity=current_quantity)
    
    product = await get_product_by_id(product_id)
    if product:
        try:
            if product.file_id:
                caption = f"**{product.title}**\n\n{product.description}\n\n**Price: {product.price} so'm**\n\n{_('Select quantity:')}"
                await call.message.edit_caption(
                    caption=caption,
                    reply_markup=await get_quantity_keyboard(product.id, current_quantity)
                )
            else:
                text = f"**{product.title}**\n\n{product.description}\n\n**Price: {product.price} so'm**\n\n{_('Select quantity:')}"
                await call.message.edit_text(
                    text,
                    reply_markup=await get_quantity_keyboard(product.id, current_quantity)
                )
        except:
            await call.answer(_("Updated"), show_alert=False)

@router.callback_query(F.data.startswith("decrease_"), OrderState.quantity)
async def decrease_quantity(call: CallbackQuery, state: FSMContext):
    product_id = int(call.data.split("_")[1])
    data = await state.get_data()
    
    current_quantity = data.get('current_quantity', 1)
    current_quantity -= 1
    
    if current_quantity < 1:
        current_quantity = 1
        await call.answer(_("Minimum quantity is 1"), show_alert=False)
    
    await state.update_data(current_quantity=current_quantity)
    
    product = await get_product_by_id(product_id)
    if product:
        try:
            if product.file_id:
                caption = f"**{product.title}**\n\n{product.description}\n\n**Price: {product.price} so'm**\n\n{_('Select quantity:')}"
                await call.message.edit_caption(
                    caption=caption,
                    reply_markup=await get_quantity_keyboard(product.id, current_quantity)
                )
            else:
                text = f"**{product.title}**\n\n{product.description}\n\n**Price: {product.price} so'm**\n\n{_('Select quantity:')}"
                await call.message.edit_text(
                    text,
                    reply_markup=await get_quantity_keyboard(product.id, current_quantity)
                )
        except:
            await call.answer(_("Updated"), show_alert=False)

@router.callback_query(F.data.startswith("add_"), OrderState.quantity)
async def add_to_cart(call: CallbackQuery, state: FSMContext):
    parts = call.data.split("_")
    product_id = int(parts[1])
    quantity = int(parts[2])
    
    product = await get_product_by_id(product_id)
    if not product:
        await call.answer(_("Product not found"), show_alert=True)
        return
    
    data = await state.get_data()
    cart = data.get('cart', [])
    
    product_in_cart = False
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += quantity
            item['total'] = item['price'] * item['quantity']
            product_in_cart = True
            break
    
    if not product_in_cart:
        cart.append({
            'product_id': product_id,
            'title': product.title,
            'price': float(product.price),
            'quantity': quantity,
            'total': float(product.price) * quantity
        })
    
    await state.update_data(cart=cart)
    
    total = sum(item['total'] for item in cart)
    
    success_text = _('Product "{product_title}" successfully added to cart ✅').format(product_title=product.title)
    await call.answer(success_text, show_alert=False)
    
    cart_text = _("🛒 Your Cart:\n\n")
    for i, item in enumerate(cart, 1):
        cart_text += f"{i}. {item['title']}\n{item['quantity']} x {item['price']:,.0f} = {item['total']:,.0f} so'm\n\n"
    
    cart_text += _("**Total: {total:,.0f} so'm**").format(total=total)
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    cart_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ " + _("Continue shopping"), callback_data="continue_shopping"),
            InlineKeyboardButton(text="✅ " + _("Complete order"), callback_data="complete_order"),
        ],
        [
            InlineKeyboardButton(text="🗑 " + _("Clear cart"), callback_data="clear_cart"),
        ]
    ])
    
    await call.message.answer(cart_text, reply_markup=cart_keyboard)
    await state.set_state(OrderState.cart)

@router.callback_query(F.data == "back_to_products", OrderState.quantity)
async def back_to_products(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category_id = data.get('category_id')
    
    if category_id:
        products = await get_products_by_category(category_id)
        if products:
            await call.message.edit_text(
                _("Please choose a product:"),
                reply_markup=await get_products_keyboard(products)
            )
            await state.set_state(OrderState.product)
        else:
            await call.answer(_("No products available"), show_alert=True)
    else:
        categories = await get_categories()
        if categories:
            await call.message.edit_text(
                _("Please choose a category:"),
                reply_markup=await get_categories_keyboard(categories)
            )
            await state.set_state(OrderState.category)
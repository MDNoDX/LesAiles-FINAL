from asgiref.sync import sync_to_async
from decimal import Decimal
from bot.models.order import Order, OrderItem
from bot.models.user import TelegramUser
from bot.models.product import Product
from bot.models.branch import Branch

@sync_to_async
def create_order(user_id, order_data):
    try:
        user = TelegramUser.objects.get(user_id=user_id)
        cart = order_data.get('cart', [])
        
        if not cart:
            return None
        
        total_amount = sum(item['total'] for item in cart)
        
        branch = None
        branch_id = order_data.get('branch_id')
        if branch_id:
            try:
                branch = Branch.objects.get(id=branch_id)
            except Branch.DoesNotExist:
                pass
        
        order = Order.objects.create(
            user=user,
            branch=branch,
            order_type=order_data.get('order_type', 'takeaway'),
            total_amount=Decimal(total_amount),
            payment_method=order_data.get('payment_method', 'cash'),
            delivery_address=order_data.get('delivery_address'),
            contact_phone=order_data.get('contact_phone', ''),
            comment=order_data.get('comment', '')
        )
        
        for item in cart:
            try:
                product = Product.objects.get(id=item['product_id'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=Decimal(item['price'])
                )
            except Product.DoesNotExist:
                continue
        
        return order
    except Exception as e:
        print(f"Error creating order: {e}")
        return None

@sync_to_async
def get_user_orders(user_id, limit=10):
    try:
        user = TelegramUser.objects.get(user_id=user_id)
        orders = Order.objects.filter(user=user).order_by('-created_at')[:limit]
        return list(orders)
    except TelegramUser.DoesNotExist:
        return []

@sync_to_async
def get_order_by_id(order_id):
    try:
        return Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return None
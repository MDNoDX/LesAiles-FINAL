from asgiref.sync import sync_to_async
from bot.models.product import Product, Category

@sync_to_async
def get_all_products(status=True):
    return list(Product.objects.filter(status=status))

@sync_to_async
def get_product_by_id(product_id):
    try:
        return Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return None

@sync_to_async
def get_categories():
    return list(Category.objects.all())

@sync_to_async
def get_products_by_category(category_id):
    return list(Product.objects.filter(category_id=category_id, status=True))

@sync_to_async
def get_product_by_telegram_id(telegram_post_id):
    try:
        return Product.objects.get(telegram_post_id=telegram_post_id)
    except Product.DoesNotExist:
        return None
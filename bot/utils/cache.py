from asgiref.sync import sync_to_async
from django.core.cache import cache
from bot.models.product import Category, Product
from bot.models.branch import Branch

CACHE_TIMEOUT = 60 * 5

@sync_to_async
def get_categories_cached():
    cache_key = 'all_categories'
    categories = cache.get(cache_key)
    if not categories:
        categories = list(Category.objects.all())
        cache.set(cache_key, categories, CACHE_TIMEOUT)
    return categories

@sync_to_async
def get_products_by_category_cached(category_id):
    cache_key = f'products_category_{category_id}'
    products = cache.get(cache_key)
    if not products:
        products = list(Product.objects.filter(category_id=category_id, status=True))
        cache.set(cache_key, products, CACHE_TIMEOUT)
    return products

@sync_to_async
def get_all_branches_cached():
    cache_key = 'all_branches'
    branches = cache.get(cache_key)
    if not branches:
        branches = list(Branch.objects.filter(is_active=True))
        cache.set(cache_key, branches, CACHE_TIMEOUT)
    return branches
from django.core.management.base import BaseCommand
from asgiref.sync import sync_to_async
import asyncio
import os
import django
from aiogram import Bot
from aiogram.types import BufferedInputFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from bot.models.product import Product, Category
from bot.models.base import City
from bot.models.branch import Branch
from core import config

class Command(BaseCommand):
    help = 'Load initial data (cities, categories, sample products, branches)'

    def handle(self, *args, **options):
        asyncio.run(self.load_initial_data())

    async def load_initial_data(self):
        # 1. Load cities
        await self.load_cities()
        
        # 2. Load branches
        await self.load_branches()
        
        # 3. Load categories
        await self.load_categories()
        
        # 4. Load sample products
        await self.load_sample_products()
        
        self.stdout.write(self.style.SUCCESS('✅ All initial data loaded successfully!'))

    @sync_to_async
    def load_cities(self):
        cities = [
            "Tashkent",
            "Andijan",
            "Samarkand",
            "Bukhara",
            "Fergana",
            "Namangan",
            "Karshi",
            "Nukus",
            "Urgench",
            "Jizzakh",
            "Navoi",
            "Termez",
            "Khiva",
            "Kokand",
        ]
        
        for city_name in cities:
            city, created = City.objects.get_or_create(name=city_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ City {city.name} created'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️ City {city.name} already exists'))

    @sync_to_async
    def load_branches(self):
        # Sample branches data
        branches_data = [
            {
                'name': 'Les Ailes Tashkent City',
                'city': City.objects.get(name='Tashkent'),
                'latitude': 41.2995,
                'longitude': 69.2401,
                'address': 'Tashkent City, Mustaqillik shoh ko\'chasi',
                'phone': '+998 71 200 00 00',
                'opening_hours': '09:00 - 23:00'
            },
            {
                'name': 'Les Ailes Samarkand',
                'city': City.objects.get(name='Samarkand'),
                'latitude': 39.6540,
                'longitude': 66.9758,
                'address': 'Samarkand, Registon maydoni',
                'phone': '+998 66 233 33 33',
                'opening_hours': '09:00 - 22:00'
            },
            {
                'name': 'Les Ailes Bukhara',
                'city': City.objects.get(name='Bukhara'),
                'latitude': 39.7681,
                'longitude': 64.4556,
                'address': 'Bukhara, Lyabi-Hauz',
                'phone': '+998 65 244 44 44',
                'opening_hours': '10:00 - 22:00'
            }
        ]
        
        for branch_data in branches_data:
            branch, created = Branch.objects.get_or_create(
                name=branch_data['name'],
                defaults=branch_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Branch {branch.name} created'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️ Branch {branch.name} already exists'))

    @sync_to_async
    def load_categories(self):
        categories = [
            "Burgers",
            "Pizzas",
            "Salads",
            "Drinks",
            "Desserts",
            "Combos",
            "Breakfast",
            "Special Offers"
        ]
        
        for category_name in categories:
            category, created = Category.objects.get_or_create(
                title=category_name,
                defaults={'title': category_name}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Category {category.title} created'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️ Category {category.title} already exists'))

    async def load_sample_products(self):
        bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
        
        # Sample products data - WITHOUT images
        products_data = [
            {
                'title': 'Classic Burger',
                'price': 25000,
                'category': 'Burgers',
                'description': 'Juicy beef patty with fresh vegetables and special sauce'
            },
            {
                'title': 'Cheeseburger',
                'price': 28000,
                'category': 'Burgers',
                'description': 'Beef patty with melted cheese, lettuce and tomato'
            },
            {
                'title': 'Chicken Burger',
                'price': 23000,
                'category': 'Burgers',
                'description': 'Crispy chicken fillet with fresh vegetables'
            },
            {
                'title': 'Margarita Pizza',
                'price': 45000,
                'category': 'Pizzas',
                'description': 'Classic pizza with tomato sauce and mozzarella'
            },
            {
                'title': 'Pepperoni Pizza',
                'price': 55000,
                'category': 'Pizzas',
                'description': 'Pizza with spicy pepperoni and cheese'
            },
            {
                'title': 'Caesar Salad',
                'price': 32000,
                'category': 'Salads',
                'description': 'Fresh salad with chicken, croutons and Caesar sauce'
            },
            {
                'title': 'Coca-Cola',
                'price': 8000,
                'category': 'Drinks',
                'description': '0.5L bottle'
            },
            {
                'title': 'Fanta',
                'price': 8000,
                'category': 'Drinks',
                'description': '0.5L bottle'
            },
            {
                'title': 'Ice Cream',
                'price': 15000,
                'category': 'Desserts',
                'description': 'Vanilla ice cream with chocolate syrup'
            },
            {
                'title': 'Combo #1',
                'price': 65000,
                'category': 'Combos',
                'description': 'Burger + Fries + Drink'
            }
        ]
        
        for product_data in products_data:
            try:
                category = await sync_to_async(Category.objects.get)(
                    title=product_data['category']
                )
                
                product, created = await sync_to_async(Product.objects.get_or_create)(
                    title=product_data['title'],
                    defaults={
                        'title': product_data['title'],
                        'price': product_data['price'],
                        'description': product_data['description'],
                        'category': category,
                        'status': True
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'✅ Product {product.title} created'))
                else:
                    self.stdout.write(self.style.WARNING(f'⚠️ Product {product.title} already exists'))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error creating product {product_data["title"]}: {str(e)}'))
        
        await bot.session.close()
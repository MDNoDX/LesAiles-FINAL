from django.core.management.base import BaseCommand
from asgiref.sync import sync_to_async
import asyncio
import os
import django
from aiogram import Bot

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from bot.models.product import Product, Category
from bot.models.base import City
from core import config

class Command(BaseCommand):
    help = 'Load products from Telegram channel'

    def handle(self, *args, **options):
        asyncio.run(self.load_products())

    async def load_products(self):
        bot = Bot(token=config.TELEGRAM_BOT_TOKEN)

        cities = ["Toshkent", "Andijon", "Samarqand", "Buxoro", "Farg'ona", "Namangan", "Qarshi", "Nukus", "Urganch"]
        
        for city_name in cities:
            city, created = await sync_to_async(City.objects.get_or_create)(name=city_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ City {city.name} created'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️ City {city.name} already exists'))

        channel_id = -1003358780776
        post_ids = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        
        product_data = {
            2: {"title": "Cheeseburger", "price": 22000, "category": "Burgers"},
            3: {"title": "Chickenburger", "price": 25000, "category": "Burgers"},
            4: {"title": "Classic Burger", "price": 20000, "category": "Burgers"},
            5: {"title": "Combo Free Burger Kola", "price": 35000, "category": "Combos"},
            6: {"title": "Combo Double Burger Double Cola", "price": 45000, "category": "Combos"},
            7: {"title": "Combo Pizza Free Gamburger Suv", "price": 50000, "category": "Combos"},
            8: {"title": "Big Burger", "price": 30000, "category": "Burgers"},
            9: {"title": "Drinks", "price": 8000, "category": "Drinks"},
            10: {"title": "Free", "price": 0, "category": "Specials"},
            11: {"title": "Spicy Burger", "price": 28000, "category": "Burgers"},
        }

        for post_id in post_ids:
            try:

                message = await bot.forward_message(
                    chat_id=-1003358780776,
                    from_chat_id=channel_id,
                    message_id=post_id
                )
                
                if message.photo:
                    file_id = message.photo[-1].file_id
                    caption = message.caption or f"{product_data[post_id]['title']} - {product_data[post_id]['price']} so'm"
                    
                    category_name = product_data[post_id]["category"]
                    category, created = await sync_to_async(Category.objects.get_or_create)(
                        title=category_name,
                        defaults={'title': category_name}
                    )
                    
                    product, created = await sync_to_async(Product.objects.get_or_create)(
                        telegram_post_id=post_id,
                        defaults={
                            'title': product_data[post_id]["title"],
                            'price': product_data[post_id]["price"],
                            'description': caption,
                            'file_id': file_id,
                            'caption': caption,
                            'category': category
                        }
                    )
                    
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'✅ Product {product.title} loaded successfully'))
                    else:
                        if not product.file_id:
                            product.file_id = file_id
                            await sync_to_async(product.save)()
                            self.stdout.write(self.style.SUCCESS(f'✅ Product {product.title} file_id updated'))
                        else:
                            self.stdout.write(self.style.WARNING(f'⚠️ Product {product.title} already exists'))
                else:
                    self.stdout.write(self.style.ERROR(f'❌ Post {post_id} has no photo'))
                        
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error loading post {post_id}: {str(e)}'))
        
        await bot.session.close()
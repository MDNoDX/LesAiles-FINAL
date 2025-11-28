import asyncio
import os
from aiogram.types import BufferedInputFile
from django.contrib import admin
from bot.apps import BotConfig
from bot.models.base import City
from bot.models.product import Product, Category
from core import config

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'caption']
    readonly_fields = ['file_id', 'created_at']

    def save_model(self, request, obj, form, change):
        if obj.temp_file and not obj.file_id:
            try:
                file_id = self._upload_to_telegram(obj.temp_file, obj.caption)
                
                existing = Product.objects.filter(file_id=file_id).first()
                if existing:
                    obj.temp_file.delete(save=False)
                    self.message_user(
                        request,
                        f"This image already exists in the database (ID: {existing.id}). File ID: {file_id}",
                        level='WARNING'
                    )
                    return

                obj.file_id = file_id
                super().save_model(request, obj, form, change)

                if obj.temp_file:
                    obj.temp_file.delete(save=False)

                self.message_user(
                    request,
                    f"✅ Image uploaded to Telegram successfully! File ID: {file_id}",
                    level='SUCCESS'
                )

            except Exception as e:
                if obj.temp_file:
                    obj.temp_file.delete(save=False)
                self.message_user(
                    request,
                    f"❌ Error uploading to Telegram: {str(e)}",
                    level='ERROR'
                )
                raise
        else:
            super().save_model(request, obj, form, change)

    def _upload_to_telegram(self, file_field, caption=None):
        storage_chat_id = getattr(config, 'TELEGRAM_STORAGE_CHAT_ID', None)
        if not storage_chat_id:
            raise ValueError("TELEGRAM_STORAGE_CHAT_ID not set in settings.")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            file_field.seek(0)
            file_content = file_field.read()
            file_name = os.path.basename(file_field.name)
            input_file = BufferedInputFile(file=file_content, filename=file_name)
            result = loop.run_until_complete(
                self._send_to_telegram(BotConfig.bot, storage_chat_id, input_file, caption)
            )
            return result['file_id']
        finally:
            loop.close()

    @staticmethod
    async def _send_to_telegram(bot, chat_id, input_file, caption):
        message = await bot.send_photo(chat_id=chat_id, photo=input_file, caption=caption)
        return {
            'file_id': message.photo[-1].file_id
        }

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title']

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
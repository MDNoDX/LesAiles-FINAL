import asyncio
import os
from aiogram.types import BufferedInputFile
from django.contrib import admin
from django.utils.html import format_html
from bot.apps import BotConfig
from bot.models.base import City
from bot.models.product import Product, Category
from bot.models.branch import Branch
from bot.models.order import Order, OrderItem
from core import config

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'category', 'has_image', 'created_at']
    list_filter = ['category', 'status', 'created_at']
    search_fields = ['title', 'description', 'caption']
    readonly_fields = ['file_id', 'created_at', 'updated_at', 'image_preview']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'price', 'category', 'description', 'status')
        }),
        ('Image Management', {
            'fields': ('temp_file', 'image_preview', 'file_id')
        }),
        ('Telegram Information', {
            'fields': ('telegram_post_id', 'caption')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def has_image(self, obj):
        return '✅' if obj.file_id else '❌'
    has_image.short_description = 'Has Image'
    
    def image_preview(self, obj):
        if obj.file_id:
            return format_html(f'<img src="https://api.telegram.org/file/bot{config.TELEGRAM_BOT_TOKEN}/getFile?file_id={obj.file_id}" width="200" />')
        return "No image"
    image_preview.short_description = 'Preview'
    
    def save_model(self, request, obj, form, change):
        if obj.temp_file and not obj.file_id:
            try:
                file_id = self._upload_to_telegram(obj.temp_file, obj.caption or f"{obj.title} - {obj.price} so'm")
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
            'file_id': message.photo[-1].file_id,
            'message_id': message.message_id
        }

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'address', 'phone', 'is_active']
    list_filter = ['city', 'is_active']
    search_fields = ['name', 'address', 'phone']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'product_count', 'created_at']
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_info', 'total_amount', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['user__first_name', 'user__username', 'contact_phone']
    readonly_fields = ['created_at', 'updated_at']
    
    def user_info(self, obj):
        return f"{obj.user.first_name} (@{obj.user.username})" if obj.user.username else obj.user.first_name
    user_info.short_description = 'User'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price', 'total_amount']
    list_filter = ['order__status']
    
    def total_amount(self, obj):
        return obj.total
    total_amount.short_description = 'Total Amount'
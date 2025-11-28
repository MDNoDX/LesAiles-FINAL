from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions
from bot.models.base import City

@register(City)
class NewsTranslationOptions(TranslationOptions):
    fields = ('name',)
from asgiref.sync import sync_to_async
from django.db.models import Q
from bot.models.base import City

@sync_to_async
def get_all_cities():
    return list(City.objects.all())

@sync_to_async
def get_city(city_name: str):
    try:
        return City.objects.get(name__iexact=city_name)
    except City.DoesNotExist:
        pass

    cities = City.objects.all()
    for city in cities:
        if city_name.lower().strip() in city.name.lower():
            return city
    
    return None
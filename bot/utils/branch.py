from asgiref.sync import sync_to_async
import math
from bot.models.branch import Branch

@sync_to_async
def get_nearest_branch(user_lat, user_lon, city_id=None):
    branches = Branch.objects.filter(is_active=True)
    if city_id:
        branches = branches.filter(city_id=city_id)
    
    nearest = None
    min_distance = float('inf')
    
    for branch in branches:
        distance = math.sqrt(
            (user_lat - branch.latitude) ** 2 + 
            (user_lon - branch.longitude) ** 2
        ) * 111.32
        
        if distance < min_distance:
            min_distance = distance
            nearest = branch
    
    return nearest, min_distance

@sync_to_async
def get_branches_by_city(city_id):
    return list(Branch.objects.filter(city_id=city_id, is_active=True))

@sync_to_async
def get_branch_by_id(branch_id):
    try:
        return Branch.objects.get(id=branch_id, is_active=True)
    except Branch.DoesNotExist:
        return None

@sync_to_async
def get_all_branches():
    return list(Branch.objects.filter(is_active=True))
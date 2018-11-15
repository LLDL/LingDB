from random import randint
from .models import Adult, Child, Family
import django.contrib.auth.models

def make_unique_id():
    potentially_random = randint(100000, 999999)
    print(potentially_random)
    isUnique = False
    while(isUnique == False):
        adult_exists = Adult.objects.filter(pk=potentially_random).exists()
        child_exists = Child.objects.filter(pk=potentially_random).exists()
        family_exists = Family.objects.filter(pk=potentially_random).exists()
        if(adult_exists or child_exists or family_exists):
            potentially_random = randint(100000, 999999)
        else:
            isUnique = True
    return str(potentially_random)

def get_user_groups(request):
    groups = request.user.groups.values_list('id', flat=True)
    print(groups)
    return groups

def get_user_queryset(request, full_queryset):
    groups = request.user.groups.values_list('id', flat=True)
    user_queryset = []
    for obj in full_queryset:
        for group in groups:
            if obj.lab.group.id == group:
                user_queryset.append(obj)
                break
    return user_queryset

def check_user_groups(request, obj):
    groups = request.user.groups.values_list('id', flat=True)
    for group in groups:
        if obj.lab.group.id == group:
            return True
    return False
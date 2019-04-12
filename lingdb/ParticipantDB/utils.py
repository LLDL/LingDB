from random import randint
from .models import Adult, Child, Family
import django.contrib.auth.models
from operator import attrgetter

def make_unique_id():
    potentially_random = randint(1000000, 9999999)
    # print(potentially_random)
    isUnique = False
    while(isUnique == False):
        adult_exists = Adult.objects.filter(pk=potentially_random).exists()
        child_exists = Child.objects.filter(pk=potentially_random).exists()
        family_exists = Family.objects.filter(pk=potentially_random).exists()
        if(adult_exists or child_exists or family_exists):
            potentially_random = randint(1000000, 9999999)
        else:
            isUnique = True
    return str(potentially_random)

def get_user_groups(request):
    groups = request.user.groups.values_list('name', flat=True)
    # print(groups)
    return groups


def get_user_authed_list(request, full_queryset, sub_of=""):
    # print(full_queryset)
    groups = request.user.groups.values_list('id', flat=True)
    user_authed_list = []
    if sub_of:
        sub_of += ".lab.group.id"
        for obj in full_queryset:
            # print(obj)
            parent = attrgetter(sub_of)(obj)
            # print("Assessment Group: ", parent)
            for group in groups:
                # print("Curr Group: ", group)
                if parent == group:
                    user_authed_list.append(obj)
    else:
        for obj in full_queryset:
            for group in groups:
                if obj.lab.group.id == group:
                    user_authed_list.append(obj)
                    break
    # print(user_authed_list)
    return user_authed_list

def check_user_groups(request, obj, sub_of=""):
    groups = request.user.groups.values_list('id', flat=True)
    if sub_of:
        sub_of += ".lab.group.id"
        parent = attrgetter(sub_of)(obj)
        for group in groups:
            if group == parent:
                return True
    else:
        for group in groups:
            if obj.lab.group.id == group:
                return True
    return False
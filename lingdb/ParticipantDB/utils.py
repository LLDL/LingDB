from random import randint
from .models import Adult, Child

def make_unique_id():
    potentially_random = randint(100000, 999999)
    print(potentially_random)
    isUnique = False
    while(isUnique == False):
        adult_exists = Adult.objects.filter(pk=potentially_random).exists()
        child_exists = Child.objects.filter(pk=potentially_random).exists()
        if(adult_exists or child_exists):
            potentially_random = randint(100000, 999999)
            print(potentially_random)
        else:
            isUnique = True
    return str(potentially_random)


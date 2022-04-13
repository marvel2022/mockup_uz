from random import randint

from .models import CustomToken



def code_generator():
    confirmation_code = randint(10000, 99999)
    while 1:
        if CustomToken.objects.filter(confirmation_code=confirmation_code).exists():
            confirmation_code = randint(10000, 99999)
        else:
            break
    return confirmation_code
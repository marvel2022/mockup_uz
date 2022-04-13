from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
# User = get_user_model()

from .models import (
    User,
    UserInfo,
)


# def post_save_user_receiver(sender, instance, created, **kwargs):
#     phone_number = instance
#     print(phone_number)
#     print(created)
#     if created:
#         user_info = UserInfo.objects.create(phone_number=phone_number)
#         user_info.save()
#         print('user info model created')

# post_save.connect(post_save_user_receiver, sender=User) 

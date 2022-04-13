from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.utils import timezone
import binascii
import os

from .manager import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    image            = models.ImageField(_('Image'), upload_to='user-image/', blank=True, null=True)
    full_name        = models.CharField(_('Full Name'), max_length=255, null=True)
    phone_number     = PhoneNumberField(_('Phone Number'), unique=True)
    email            = models.EmailField(_('Email'), blank=True, null=True)
    address          = models.CharField(_('Address'), max_length=255, blank=True, null=True)
    company          = models.CharField(_('Company'), max_length=255, blank=True, null=True)
    company_web_site = models.URLField(_('Company Web Site'), blank=True, null=True)
    company_address  = models.CharField(_('Company Address'), max_length=255, blank=True, null=True)

    is_staff              = models.BooleanField(_('is_staff'), default=False)
    is_superuser          = models.BooleanField(_('is_superuser'), default=False)
    is_active             = models.BooleanField(_('is_active'), default=True)
    last_login            = models.DateTimeField(_('last_login'), auto_now=True, null=True, blank=True)
    date_joined           = models.DateTimeField(_("date_joined"), auto_now_add=True)
    phone_number_verified = models.BooleanField(default=False)
    change_pw             = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD     = 'phone_number'
    PHONE_NUMBER_FIELD = 'phone_number'
    # REQUIRED_FIELDS    = ['full_name',]

    class Meta:
        ordering            = ('phone_number',)
        verbose_name        = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        if self.full_name:
            return self.full_name +" | " + str(self.phone_number) 
        return str(self.phone_number)

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url=''
        return url

def post_save_user_receiver(sender, instance, created, **kwargs):
    phone_number = instance
    if created:
        user = User.objects.get(phone_number=instance.phone_number)
        user.phone_number_verified = True

post_save.connect(post_save_user_receiver, sender=User)


class CustomToken(models.Model):
    """
    The default authorization token model.
    """
    key               = models.CharField(_("Key"), max_length=40, unique=True)
    phone_number      = PhoneNumberField(_('Phone Number'))
    confirmation_code = models.SmallIntegerField(_('Confirmation Code'), blank=True, null=True)
    session_key       = models.CharField(_("Session Key"), max_length=200, blank=True, null=True)
    client_ip         = models.CharField(_("Client Ip"), max_length=50, blank=True, null=True)

    created = models.DateTimeField(_("Created"), default=timezone.now)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
            while 1:
                if CustomToken.objects.filter(key=self.key).exists():
                    self.key = self.generate_key()
                else:
                    break
        return super(CustomToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
    
    @property
    def check_valid_token(self):
        if self.created < timezone.now()-timezone.timedelta(minutes=5):
            e = CustomToken.objects.get(pk=self.pk)
            e.delete()
            return False
        else:
            return True
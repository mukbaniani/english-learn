from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class CustumUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError(_('მეილის შეყვანა აუცილებელია'))
        if not username:
            raise ValueError(_('მომხმარებელი აუცილებელია'))
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError(_('მეილის შეყვანა აუცილებელია'))
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(max_length=25, verbose_name=_('მომხმარებელი'))
    email = models.EmailField(verbose_name=_('მეილი'), unique=True)
    password = models.CharField(max_length=255, verbose_name=_('პაროლი'))
    phone_number = models.CharField(max_length=13, verbose_name=_('ტელეფონის ნომერი'), blank=True, null=True)

    def __str__(self):
        return f"{self.__class__.__name__}('{self.username}', '{self.email}')"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustumUserManager()

    class Meta:
        verbose_name = _('მომხმარებელი')

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

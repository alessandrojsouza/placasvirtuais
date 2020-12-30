from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
  siape = models.CharField('Siape', max_length=300, null=False, blank=False)
  
  class Meta(AbstractUser.Meta):
    swappable = 'AUTH_USER_MODEL'

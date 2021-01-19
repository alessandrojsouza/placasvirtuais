from django.db import models

from django.urls import reverse

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
  # siape = models.CharField('Siape', max_length=300, null=False, blank=False)
  
  class Meta(AbstractUser.Meta):
    swappable = 'AUTH_USER_MODEL'

  def get_create_url(self):
    return reverse('core:create')
    
  def get_update_url(self):
    return reverse('core:update', kwargs={'pk': self.pk})

  def get_absolute_url(self):
    return reverse('core:list')

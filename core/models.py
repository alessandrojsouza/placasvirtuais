from django.db import models

from django.conf import settings

from django.utils.translation import ugettext as _
from django.urls import reverse

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
  avatar = models.ImageField(_('Avatar'), upload_to='user/', null=True, blank=True)
  campus = models.CharField(_('Campus'), null=True, blank=True, max_length=10)
  
  class Meta(AbstractUser.Meta):
    swappable = 'AUTH_USER_MODEL'

  def get_create_url(self):
    return reverse('core:create')
    
  def get_update_url(self):
    return reverse('core:update', kwargs={'pk': self.pk})
  
  def get_preview_url(self):
    return reverse('core:preview', kwargs={'pk': self.pk})

  def get_absolute_url(self):
    return reverse('core:list')

  def get_avatar(self):
    if self.avatar and self.is_authenticated:
      return '{0}{1}'.format(settings.MEDIA_URL, self.avatar)

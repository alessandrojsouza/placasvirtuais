from django.db import models

from django.urls import reverse

from django.utils.translation import ugettext as _


class Campus(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  name = models.CharField(_('Nome'), max_length=300)
  abbreviation = models.CharField(_('Sigla'), max_length=300)
  
  class Meta:
    verbose_name = _(u'Campus')
    verbose_name_plural = _(u'Campus')

  def __str__(self):
    return '{0.name}'.format(self)

  def get_create_url(self):
    return reverse('campus:create')
    
  def get_update_url(self):
    return reverse('campus:update', kwargs={'pk': self.pk})
  
  def get_preview_url(self):
    return reverse('campus:preview', kwargs={'pk': self.pk})

  def get_absolute_url(self):
    return reverse('campus:list')
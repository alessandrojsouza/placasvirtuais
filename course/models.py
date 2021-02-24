from django.db import models

from django.urls import reverse

from django.utils.translation import ugettext as _


class Course(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  name = models.CharField(_('Nome'), max_length=300)
  code = models.CharField(_('Código'), max_length=300)

  class Meta:
    verbose_name = _(u'Curso')
    verbose_name_plural = _(u'Cursos')

  def __str__(self):
    return '{0.name}'.format(self)

  def get_create_url(self):
    return reverse('course:create')
    
  def get_update_url(self):
    return reverse('course:update', kwargs={'pk': self.pk})
  
  def get_preview_url(self):
    return reverse('course:preview', kwargs={'pk': self.pk})

  def get_absolute_url(self):
    return reverse('course:list')
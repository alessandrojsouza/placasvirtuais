from django.db import models

from django.urls import reverse

from django.utils.translation import ugettext as _

from board.models import Board

from core.serializers import Base64ImageField


class Egress(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  name = models.CharField(_('Nome'), max_length=300)
  enrollment = models.CharField(_('Matricula'), max_length=300)
  lattes = models.CharField(_('Lattes'), max_length=300)
  email = models.CharField(_('Email'), max_length=300)
  social_network = models.CharField(_('Rede social'), max_length=300)
  board = models.ForeignKey(Board, on_delete=models.CASCADE)
  photo = models.ImageField(_('Imagem'), upload_to='egress/', blank=True, null=True)  
  image = Base64ImageField(max_length=None, use_url=True)

  class Meta:
    verbose_name = _(u'Egresso')
    verbose_name_plural = _(u'Egressos')

  def __str__(self):
    return '{0.name}'.format(self)

  def get_create_url(self):
    return reverse('egress:create')
    
  def get_update_url(self):
    return reverse('egress:update', kwargs={'pk': self.pk})
  
  def get_preview_url(self):
    return reverse('egress:preview', kwargs={'pk': self.pk})

  def get_absolute_url(self):
    return reverse('egress:list')

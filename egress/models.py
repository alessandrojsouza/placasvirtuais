from django.db import models

from django.utils.translation import ugettext as _

from board.models import Board


class Egress(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  name = models.CharField(_('Nome'), max_length=300)
  enrollment = models.CharField(_('Matricula'), max_length=300)
  photo = models.ImageField(_('Imagem'), upload_to='egress')
  lattes = models.CharField(_('Lattes'), max_length=300)
  email = models.CharField(_('Email'), max_length=300)
  social_network = models.CharField(_('Rede social'), max_length=300)

  board = models.ForeignKey(Board, on_delete=models.CASCADE)

  class Meta:
    verbose_name = _(u'Egresso')
    verbose_name_plural = _(u'Egressos')

  def __str__(self):
    return '{0.name}'.format(self)

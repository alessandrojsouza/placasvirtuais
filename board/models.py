from django.db import models

from django.utils.translation import ugettext as _

import datetime


def current_year():
  return datetime.date.today().year


class Board(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  name = models.CharField(_('Nome'), max_length=300)
  photo = models.ImageField(_('Imagem'), upload_to='boards')
  message = models.TextField(
    _('Mensagem'), null=True, blank=True)
  year_graduation = models.IntegerField(_('Ano do período'), default=current_year)
  graduation_date = models.DateTimeField(_('Data da formatura'), auto_now_add=False)

  class Meta:
    verbose_name = _(u'Board')
    verbose_name_plural = _(u'Boards')

  def __str__(self):
    return '{0.name}'.format(self)

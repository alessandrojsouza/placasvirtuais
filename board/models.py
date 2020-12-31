from django.db import models

from django.utils.translation import ugettext as _
from course.models import Course
from mentioned.models import Mentioned
from campus.models import Campus

import datetime


def current_year():
  return datetime.date.today().year


class Board(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  name = models.CharField(_('Nome'), max_length=300)
  photo = models.ImageField(_('Imagem'), upload_to='board/images/')
  message = models.TextField(
    _('Mensagem'), null=True, blank=True)
  year_graduation = models.IntegerField(_('Ano do período'), default=current_year)
  graduation_date = models.DateTimeField(_('Data da formatura'), auto_now_add=False)
  
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
  mentioned = models.ManyToManyField(Mentioned)

  class Meta:
    verbose_name = _(u'PLaca')
    verbose_name_plural = _(u'Placas')

  def __str__(self):
    return '{0.name}'.format(self)

from django.db import models

from django.utils.translation import ugettext as _
from course.models import Course
from campus.models import Campus

import datetime

from django.urls import reverse


def current_year():
  return datetime.date.today().year


class Board(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  name = models.CharField(_('Nome'), max_length=300)
  photo = models.ImageField(_('Imagem'), upload_to='board/')
  message = models.TextField(
    _('Mensagem'), null=True, blank=True)
  year_graduation = models.IntegerField(_('Ano do período'), default=current_year)
  # graduation_date = models.DateTimeField(_('Data da formatura'), auto_now_add=False)
  graduation_date = models.DateField(_('Data da formatura'))
  
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  # campus = models.ForeignKey(Campus, on_delete=models.CASCADE)

  # mentioned = models.ManyToManyField(Mentioned)
  mentioned = models.ManyToManyField(
    to='board.Mentioned',
    blank=True,
    verbose_name='Mencionado',
    related_name='mentioneds'
  )

  class Meta:
    verbose_name = _(u'PLaca')
    verbose_name_plural = _(u'Placas')

  def __str__(self):
    return '{0.name}'.format(self)

  def get_create_url(self):
    return reverse('board:create')
    
  def get_update_url(self):
    return reverse('board:update', kwargs={'pk': self.pk})
  
  def get_preview_url(self):
    return reverse('board:preview', kwargs={'pk': self.pk})

  def get_absolute_url(self):
    return reverse('board:list')


class Mentioned(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  siape = models.CharField(_('Siape'), max_length=300)
  name = models.CharField(_('Nome'), max_length=300)

  DEAN, PARANINFO, PATRON, DG, DE, INMEMORIAM, EMPLOYEE, HONORED, SPEAKER = range(9)
  MENTION_CHOICES = (
    (DEAN, _('Reitor')),
    (PARANINFO, _('Paraninfo')),
    (PATRON, _('Patrono')),
    (DG, _('DG')),
    (DE, _('DE')),
    (INMEMORIAM, _('Em memoria')),
    (EMPLOYEE, _('Funcionário')),
    (HONORED, _('Homenageado')),
    (SPEAKER, _('Orador')),
  )

  mention = models.SmallIntegerField(
    _('Tipo de menção'),
    choices=MENTION_CHOICES)

  class Meta:
    verbose_name = _(u'Mencionado')
    verbose_name_plural = _(u'Mencionados')

  def __str__(self):
    return '{0.name}'.format(self)

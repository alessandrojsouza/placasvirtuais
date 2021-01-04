from django.db import models

from django.utils.translation import ugettext as _


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

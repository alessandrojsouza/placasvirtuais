from django.db import models

from django.urls import reverse

from django.utils.translation import ugettext as _

from course.models import Directorship, Course
from board.models import Board


class Sending(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.EmailField(_('Email'), max_length=100)
    recipient_directorship = models.ManyToManyField(
        Directorship,
        blank=True,
        verbose_name='Diretoria',
        related_name='directorships'
    )
    recipient_board = models.ManyToManyField(
        Board,
        blank=True,
        verbose_name='Placa',
        related_name='boards'
    )
    recipient_course = models.ManyToManyField(
        Course,
        blank=True,
        verbose_name='Curso',
        related_name='courses'
    )
    recipient_year = models.CharField(_('Ano'), max_length=300)
    recipient_period = models.CharField(_('Periodo'), max_length=300)
    recipient_count = models.IntegerField(null=True)
    subject = models.CharField(_('Assunto'), max_length=100)
    message = models.CharField(_('Mensagem'), max_length=100000)
    file = models.FileField(_('File'), upload_to='sending/', blank=True, null=True)

    class Meta:
        verbose_name = _(u'Email')
        verbose_name_plural = _(u'Emails')

    def __str__(self):
        return '{0.subject}'.format(self)

    def get_create_url(self):
        return reverse('sending:create')
        
    def get_update_url(self):
        return reverse('sending:update', kwargs={'pk': self.pk})
    
    def get_preview_url(self):
        return reverse('sending:preview', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return reverse('sending:list')

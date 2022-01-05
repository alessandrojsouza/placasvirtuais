from django.db import models

from django.urls import reverse

from django.utils.translation import ugettext as _


class Email(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    
    sender = models.EmailField(_('Email'), max_length=100) # remetente - usuario ou instituicao
    # destinatario - curso(s), egressos
    # recipient_course =
    # recipient_course_period =
    # recipient_egress =
    subject = models.CharField(_('Assunto'), max_length=100)
    message = models.CharField(_('Mensagem'), max_length=50000)

    class Meta:
        verbose_name = _(u'Email')
        verbose_name_plural = _(u'Emails')

    def __str__(self):
        return '{0.subject}'.format(self)

    def get_create_url(self):
        return reverse('emails:create')
        
    def get_update_url(self):
        return reverse('emails:update', kwargs={'pk': self.pk})
    
    def get_preview_url(self):
        return reverse('emails:preview', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return reverse('emails:list')

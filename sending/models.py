from django.db import models

from django.urls import reverse

from django.utils.translation import ugettext as _


class Sending(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.EmailField(_('Email'), max_length=100)
    recipient = models.CharField(_('Emails dos Destinatarios'), max_length=100000)
    subject = models.CharField(_('Assunto'), max_length=100)
    message = models.CharField(_('Mensagem'), max_length=100000)

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

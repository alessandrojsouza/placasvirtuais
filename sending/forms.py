from django import forms

from sending.models import Sending


class SendingForm(forms.ModelForm):
    class Meta:
        model = Sending
        fields = '__all__'

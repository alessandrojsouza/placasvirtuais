from django import forms
from django.utils.translation import ugettext_lazy as _

from campus.models import Campus


class CampusForm(forms.ModelForm):
    class Meta:
        model = Campus
        fields = '__all__'

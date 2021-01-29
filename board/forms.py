from django import forms
from django.utils.translation import ugettext_lazy as _

from board.models import Board


class BoardForm(forms.ModelForm):
  class Meta:
    model = Board
    fields = '__all__'

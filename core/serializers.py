from rest_framework import serializers

from core.models import User

import base64
from django.core.files.base import ContentFile


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'


class Base64ImageField(serializers.ImageField):
  def from_native(self, data):
    if isinstance(data, basestring) and data.startswith('data:image'):
      # base64 encoded image - decode
      format, imgstr = data.split(';base64,')  # format ~= data:image/X,
      ext = format.split('/')[-1]  # guess file extension

      data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

    return super(Base64ImageField, self).from_native(data)
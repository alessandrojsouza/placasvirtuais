from rest_framework import serializers

from egress.models import Egress

from core.serializers import Base64ImageField


class EgressSerializer(serializers.ModelSerializer):
  image =  Base64ImageField()

  class Meta:
    model = Egress
    fields = ('created_at', 'name', 'enrollment', 'lattes', 'email', 'social_network', 'board', 'photo', 'image')

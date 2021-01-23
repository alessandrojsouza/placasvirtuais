from rest_framework import serializers

from egress.models import Egress


class EgressSerializer(serializers.ModelSerializer):
  class Meta:
    model = Egress
    fields = '__all__'

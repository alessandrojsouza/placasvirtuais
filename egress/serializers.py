from rest_framework import serializers

from egress.models import Egress



class EgressSerializer(serializers.ModelSerializer):

  class Meta:
    model = Egress
    fields = ('name', 'enrollment', 'lattes', 'email', 'social_network', 'board', 'photo')

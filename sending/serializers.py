from rest_framework import serializers

from sending.models import Sending


class SendingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sending
        fields = '__all__'

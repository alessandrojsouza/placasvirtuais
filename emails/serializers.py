from rest_framework import serializers

from emails.models import Emails



class EmailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Emails
        fields = ('sender', 'subject', 'message')

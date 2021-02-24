from rest_framework import serializers

from board.models import Board, Mentioned


class BoardSerializer(serializers.ModelSerializer):
  class Meta:
    model = Board
    fields = '__all__'


class MentionedSerializer(serializers.ModelSerializer):
  class Meta:
    model = Mentioned
    fields = '__all__'

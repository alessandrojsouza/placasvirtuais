from rest_framework import serializers

from course.models import Course


class CourseSerializer(serializers.ModelSerializer):
  directorship_name = serializers.CharField(source='directorship.name')
  class Meta:
    model = Course
    fields = 'id', 'created_at', 'name', 'code', 'directorship', 'directorship_name', 

from rest_framework import serializers

from .models import *


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        exclude = ['course', 'user']

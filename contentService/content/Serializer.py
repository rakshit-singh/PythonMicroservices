from django.forms import models
from rest_framework import serializers
from .models import Content

class ContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Content
        fields = '__all__'

class ContentPartialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['title', 'story']
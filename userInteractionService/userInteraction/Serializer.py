from rest_framework import serializers
from .models import ReadEvent, LikeEvent, User

class ReadEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReadEvent
        fields = '__all__'


class LikeEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = LikeEvent
        fields = ['user_id', 'title']

# TODO: Look at if this serializer is actually needed
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


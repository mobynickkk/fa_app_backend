from .models import Profile, HomeTask
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    group = serializers.CharField(read_only=True, source="group.index")

    class Meta:
        model = Profile
        fields = ['id', 'name', 'group']


class HomeTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = HomeTask
        exclude = []

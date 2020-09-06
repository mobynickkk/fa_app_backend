from .models import Profile, Subject, HomeTask
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(read_only=True, source="user.first_name")
    last_name = serializers.CharField(read_only=True, source="user.last_name")
    email = serializers.CharField(read_only=True, source="user.email")
    group = serializers.CharField(read_only=True, source="group.index")

    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name', 'email', 'group']


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        exclude = []


class HomeTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = HomeTask
        exclude = []

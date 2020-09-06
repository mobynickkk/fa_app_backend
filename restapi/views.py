from django.contrib.auth.models import User
from rest_framework import viewsets, views
from rest_framework.response import Response
from .models import Profile, Subject, HomeTask
from .serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileByEmail(views.APIView):
    def get(self, request):
        profile = Profile.objects.get(user=User.objects.get(username=request.GET['email']))
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

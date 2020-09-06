from django.contrib.auth.models import User
from rest_framework import viewsets, views, mixins, generics
from rest_framework.response import Response
from .models import Profile, Subject, HomeTask, Group
from .serializers import ProfileSerializer, HomeTaskSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileByEmail(views.APIView):
    def get(self, request):
        profile = Profile.objects.get(user=User.objects.get(username=request.GET['email']))
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class HomeTaskAPI(mixins.CreateModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = HomeTask.objects.all()
    serializer_class = HomeTaskSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = HomeTask.objects.filter(
            func=lambda task: task.group == Group.objects.get(pk=request.GET["group"])
        )
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

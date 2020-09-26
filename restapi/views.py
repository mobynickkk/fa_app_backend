from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, views, mixins, generics
from rest_framework.response import Response
from .models import Profile, HomeTask
from .serializers import ProfileSerializer, HomeTaskSerializer
from icalendar import Calendar
from datetime import datetime, timezone


def get_calendar(request):
    from json import dumps
    response = []
    with open('pm_20_4.ics', 'rb') as file:
        current_key = ''
        i = 0
        calendar = Calendar.from_ical(file.read())
        for component in calendar.walk():
            if component.name == "VEVENT":
                if component.get("dtstart").dt < datetime.now(timezone.utc):
                    continue
                dt_start = component.get("dtstart").dt.timetuple()
                dt_end = component.get("dtend").dt.timetuple()
                data_array = component.get("description").split('\n')

                lesson = {
                    'subject': str(component.get("summary")),
                    'type': data_array[0],
                    'teacher': data_array[1],
                    'place': str(component.get("location")),
                    'time': str(dt_start[3]) + ':' + str(dt_start[4]) + '-' +
                    str(dt_end[3]) + ':' + str(dt_end[4])
                }

                if not current_key or str(dt_start[1]) + '/' + str(dt_start[2]) + '/' + str(dt_start[0])[2:] != current_key:
                    response.append({
                        'key': str(dt_start[1]) + '/' + str(dt_start[2]) + '/' + str(dt_start[0])[2:],
                        'list': [lesson]
                    })
                    i += 1 if current_key else 0
                    current_key = str(dt_start[1]) + '/' + str(dt_start[2]) + '/' + str(dt_start[0])[2:]
                else:
                    response[i]['list'].append(lesson)
    return HttpResponse(dumps(response[:14]).encode())


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileByNameAndGroup(views.APIView):
    def get(self, request):
        try:
            profile = Profile.objects.get(hash=request.GET['hash'])
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return HttpResponse(404)


class HomeTaskByProfile(viewsets.ModelViewSet):
    serializer_class = HomeTaskSerializer

    def get_queryset(self):
        try:
            homework = HomeTask.objects.filter(profile__hash=self.request.GET['hash'])
            return homework
        except ObjectDoesNotExist:
            return HttpResponse(404)


class HomeTaskAPI(mixins.CreateModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = HomeTask.objects.all()
    serializer_class = HomeTaskSerializer

    def get(self, request, *args, **kwargs):
        try:
            self.queryset = HomeTask.objects.get(
                profile__hash=request.GET['hash'], pk=1
            )
            return self.retrieve(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return HttpResponse(404)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

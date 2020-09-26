from django.http import HttpResponse
from rest_framework import viewsets, views, mixins, generics
from rest_framework.response import Response
from .models import Profile, HomeTask, Group
from .serializers import ProfileSerializer, HomeTaskSerializer
from icalendar import Calendar
from datetime import datetime, timezone


def get_calendar(request):
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

                if not current_key or str(dt_start[2]) + '.' + str(dt_start[1]) != current_key:
                    response.append({
                        'key': str(dt_start[2]) + '.' + str(dt_start[1]),
                        'list': [lesson]
                    })
                    i += 1 if current_key else 0
                    current_key = str(dt_start[2]) + '.' + str(dt_start[1])
                else:
                    response[i]['list'].append(lesson)
    return HttpResponse(response)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileByNameAndGroup(views.APIView):
    def get(self, request):
        profile = Profile.objects.get(hash=request.GET['hash'])
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class HomeTaskByProfile(viewsets.ModelViewSet):
    def get(self, request):
        homework = HomeTask.objects.filter(profile__hash=request.GET['hash'])
        serializer = ProfileSerializer(homework)
        return Response(serializer.data)


class HomeTaskAPI(mixins.CreateModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = HomeTask.objects.all()
    serializer_class = HomeTaskSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = HomeTask.objects.get(
            profile__hash=request.GET['hash'], pk=1
        )
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

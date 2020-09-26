from django.urls import include, path
from rest_framework import routers
from .views import ProfileViewSet, ProfileByNameAndGroup, HomeTaskAPI, get_calendar, HomeTaskByProfile

router = routers.DefaultRouter()
router.register(r'users', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', ProfileByNameAndGroup.as_view()),
    path('hometask/', HomeTaskAPI.as_view()),
    path('schedule/', get_calendar),
    path('homework/', HomeTaskByProfile.as_view({'get': 'list'}))
]

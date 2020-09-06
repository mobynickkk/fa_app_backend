from django.urls import include, path
from rest_framework import routers
from .views import ProfileViewSet, ProfileByEmail, HomeTaskAPI

router = routers.DefaultRouter()
router.register(r'users', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', ProfileByEmail.as_view()),
    path('hometask/', HomeTaskAPI.as_view())
]
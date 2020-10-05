from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from restapi import urls as rest_urls
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(rest_urls)),
    path('api/v2/', csrf_exempt(GraphQLView.as_view(graphiql=True)))
]

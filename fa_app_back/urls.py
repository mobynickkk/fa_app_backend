from django.contrib import admin
from django.urls import path, include
from restapi import urls as rest_urls
from graphqlapi import urls as graphql_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(rest_urls)),
    path('api/v2/', include(graphql_api))
]

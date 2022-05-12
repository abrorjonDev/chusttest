from django.urls import path, include
from rest_framework.routers import DefaultRouter

#local imports




router = DefaultRouter()


urlpatterns = (
    path('', include(router.urls)),
)
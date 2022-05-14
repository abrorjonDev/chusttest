from django.urls import path, include
from rest_framework.routers import DefaultRouter

#local imports
from .views import TestCreateView, TestUpdateView, PostStudentAnswer



router = DefaultRouter()


urlpatterns = (
    path('', include(router.urls)),
    path('tests/', TestCreateView.as_view(), name="test_create_api"),
    path('tests/<int:pk>/', TestUpdateView.as_view(), name="test_update_api"),
    path('tests/answer/<int:pk>/', PostStudentAnswer.as_view(), name="post_student_answer"),
)
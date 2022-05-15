from django.urls import path, include
from rest_framework.routers import DefaultRouter

#local imports
from .views import TestReadFromFile, AllTestsViewSet, SubjectsViewSet, AnswersViewSet




router = DefaultRouter()
router.register(r'subjects', SubjectsViewSet, basename="all_subjects")
router.register(r'answers', AnswersViewSet, basename="answers_api")
router.register(r'', AllTestsViewSet, basename="all_tests")



urlpatterns = (
    path('file/', TestReadFromFile.as_view(), name="create_by_file"),
    path('', include(router.urls)),
)
from django.urls import path, include
from rest_framework.routers import DefaultRouter

#local imports
from .views import (
    TestCreateView, 
    TestUpdateView, 
    PostStudentAnswer,

    StudentStatisticsView,
    StudentResultsView,
    StatisticsView,

    OlympicsView,
    OlympicsDetailView,
    OlympicResultsView,
    OlympicTestCreateView,
    OlympicTestDetailView,
    OlympicStudentAnswerView,
    OlympicSubjectsViewSet,
)
 
 

router = DefaultRouter()
router.register(r'olympics/subjects', OlympicSubjectsViewSet, basename="Olympics_subjects")

urlpatterns = (
    path('', include(router.urls)),
    path('tests/', TestCreateView.as_view(), name="test_create_api"),
    path('tests/<int:pk>/', TestUpdateView.as_view(), name="test_update_api"),
    path('tests/answer/<int:pk>/', PostStudentAnswer.as_view(), name="post_student_answer"),

    path('statistics/me/', StudentStatisticsView.as_view(), name="student_statistics_api"),
    path('statistics/students/', StudentResultsView.as_view(), name="all_students_results_view"),
    path('statistics/', StatisticsView.as_view(), name="api_for_get_all_statistics_by_admin"),

    path('olympics/', OlympicsView.as_view(), name="olympics_api_view"),
    path('olympics/<int:pk>/', OlympicsDetailView.as_view(), name="olympics_detail_api_view"),
    path('olympics/results/<int:pk>/', OlympicResultsView.as_view(), name="olympics_results_api_view"),
    path('olympics/students/tests/', OlympicTestCreateView.as_view(), name="get_student_olympic_tests_api"),
    path('olympics/students/tests/<int:pk>/', OlympicTestDetailView.as_view(), name="get_student_tests_detail_api"),
    path('olympics/students/tests/questions/<int:pk>/', OlympicStudentAnswerView.as_view(), name="student_answer_post_api"),
    path('', include(router.urls)),
) 
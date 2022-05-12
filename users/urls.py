from django.urls import path, include
from rest_auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView

# local imports
from .views import StudentsListView, StudentDetailView, FileUpload



urlpatterns = [
    path("students/", StudentsListView.as_view(), name="students_list"),
    path("students/create/", FileUpload.as_view(), name="file_upload_student_create"),
    path("students/<int:pk>/", StudentDetailView.as_view(), name="student_detail"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('password/change/', PasswordChangeView.as_view(), name="password_change"),
    path('password/reset/', PasswordResetView.as_view(), name="password_reset"),
    path('password/reset/complete/', PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    # path('login/', LoginView.as_view(), name="login_api"),
]
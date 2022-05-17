from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from uritemplate import partial
User = get_user_model()
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from django.db.models import Q
from django.contrib.auth.hashers import PBKDF2PasswordHasher
#local imports
from .serializers import LoginSerializer, UserDataSerializer, UserListSerializer
from .file_read import create_students
from .models import UserFileModel
from .tasks import student_register_by_file
class LoginView(APIView):
    serializer_class = LoginSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    def get_queryset(self):
        return User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            return Response({'status':200, 'token':'token'}, status=200)
        return Response({'status':401, 'token':None}, status=400) 

class UserDetailView(APIView):
    def get_queryset(self):
        return User.objects.exclude(Q(is_superuser=True)|Q(is_staff=True))
    serializer_class = UserDataSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user, many=False)
        return Response(serializer.data, status=200)
    
    def patch(self, request):
        serializer = self.serializer_class(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)



class StudentsListView(APIView):
    def get_queryset(self):
        return User.objects.exclude(Q(is_superuser=True)|Q(is_staff=True))

    serializer_class = UserListSerializer #UserDataSerializer
    permission_classes = (IsAdminUser, )

    def get(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class StudentDetailView(APIView):
    """
    Update Student datas. 
    GET, PUT, PATCH, DELETE methods are enabled.
    """
    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    serializer_class = UserDataSerializer

    def get(self, request, pk):
        student = self.get_object(pk=pk)
        serializer = self.serializer_class(student, many=False)
        return Response(serializer.data, status=200)

    def put(self, request, pk):
        student = self.get_object(pk=pk)
        serializer = self.serializer_class(student,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(modified_by=request.user)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


    def patch(self, request, pk):
        student = self.get_object(pk=pk)
        serializer = self.serializer_class(student,data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(modified_by=request.user)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        student = self.get_object(pk=pk)
        try:
            student.delete()
            return Response({'status':'deleted succesfully.'}, status=200)
        except:
            return Response({'status':'Not found.'}, status=404)

class FileUpload(APIView):
    """
    THIS API IS FOR CREATING AND UPDATING STUDENTS.
    FILE UPLOAD IN XLSX FILE FORMAT.
    post file in multipart/form-data.
    """
    queryset = None
    # parser_classes = (MultiPartParser, )
    permission_classes = (IsAdminUser, )

    def post(self, request):
        file = request.data['file']
        user=request.user
        # file_model = UserFileModel.objects.create(file=file, created_by=request.user)
        # student_register_by_file.delay(file, user)
        student_status = create_students(file=file, created_by=request.user)
        return Response(student_status, status=200)
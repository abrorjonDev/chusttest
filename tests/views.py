from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

#local imports
from .models import QuestionModel, AnswerModel, Subjects
from .serializers import AnswersListSerializer, SubjectSerializer, TestCreateSerializer, TestListSerializer
from .file_read import read_new_tests

class AllTestsViewSet(ModelViewSet):
    def get_queryset(self):
        return QuestionModel.objects.all()
    serializer_class = TestListSerializer
    permission_classes = (IsAuthenticated, )
    # def list(self, request):
    #     return Response({'status':'new tests created'}, status=201)

    def create(self, request):
        return Response({'status':'new tests created'}, status=201)


class TestReadFromFile(APIView):
    """
    Upload a file which type in xlsx.
    And All tests in the file will be read and written to database. 
    """
    queryset = None
    permission_classes = (AllowAny, )


    def post(self ,request):
        file = request.data['file']
        read_new_tests(file, request=request)
        return Response({'status':'new tests created'}, status=201)


class TestDetailViewSet(ModelViewSet):
    queryset = QuestionModel
    serializer_class = TestListSerializer

    

class SubjectsViewSet(ModelViewSet):
    def get_queryset(self):
        return Subjects.objects.all()
    
    serializer_class = SubjectSerializer


from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

#local imports
from .models import QuestionModel, AnswerModel, Subjects
from .serializers import AnswersListSerializer, SubjectSerializer, TestAdminListSerializer, TestListSerializer
from .file_read import read_new_tests

 
class AllTestsViewSet(ModelViewSet):
    def get_queryset(self, subject=None, klass=None):
        if subject and klass:
            return QuestionModel.objects.filter(subject=subject, klass=klass)
        elif subject:
            return QuestionModel.objects.filter(subject=subject)
        elif klass:
            return QuestionModel.objects.filter(klass=klass)
        else:
            return QuestionModel.objects.all()

    def get_serializer_class(self, user=None):
        if user and user.is_superuser==True:
            return TestAdminListSerializer
        return TestListSerializer
    permission_classes = (IsAuthenticated, )
    
    def list(self, request):
        subject = request.query_params.get('subject', None)
        klass = request.query_params.get('klass', None)
        serializer = self.get_serializer_class(user=request.user)(self.get_queryset(subject=subject, klass=klass), many=True, context={'request':request})
        return Response(serializer.data, status=200)

    def create(self, request):
        serializer = self.get_serializer_class(user=request.user)(data=request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)



class TestReadFromFile(APIView):
    """
    Upload a file which type in xlsx.
    And All tests in the file will be read and written to database. 
    """
    queryset = None
    permission_classes = (AllowAny, )


    def post(self ,request):
        file = request.data['file']
        subject = request.data.get('subject', None)
        klass = request.data.get('klass', None)
        print(subject, klass)
        read_new_tests(file, request=request, subject=subject, klass=klass)
        return Response({'status':'new tests created'}, status=201)


class TestDetailViewSet(ModelViewSet):
    queryset = QuestionModel
    serializer_class = TestListSerializer

    

class SubjectsViewSet(ModelViewSet):
    def get_queryset(self):
        return Subjects.objects.all()
    
    serializer_class = SubjectSerializer


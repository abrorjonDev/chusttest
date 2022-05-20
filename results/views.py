from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
import random
import datetime
from django.utils import timezone

#local imports
from tests.models import QuestionModel
from .models import StudentQuestions, StudentTests, OlympicStudentTests
from .serializers import *

import os
from dotenv import load_dotenv
load_dotenv()



class TestCreateView(APIView):
    def get_queryset(self):
        return StudentTests.objects.all()

    serializer_class = TestCreateSerializer
    list_serializer_class = TestResultsSerializer
    
    def get(self, request):
        # serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response({}, status=200) 
 
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            klass = serializer.validated_data.get('klass', None)
            subject = serializer.validated_data.get('subject', None)
            tests_count = int(os.environ.get('TEST_COUNT', default=30))

            #if the questions related to the selected subject and klass aren't enough 
            # return not enough status 
            if QuestionModel.objects.filter(subject=subject, klass=klass).count()<tests_count:
                return Response({'status':'Bu fan va sinf doirasida testlar yetarli emas.', 'status_code':400}, status=200)

            now=timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
            student_tests = StudentTests.objects.filter(
                created_by=request.user, 
                subject=subject, klass=klass, 
                date_created__gte=now-datetime.timedelta(hours=1), finished=False)
            
            #last created tests by student
            if student_tests.count() > 0:
                test_obj = student_tests.first()
                
            # new creating tests                
            else:
                test_obj = StudentTests.objects.create(
                    created_by=request.user, subject=subject, klass=klass)
                
                questions = QuestionModel.objects.filter(subject=subject, klass=klass)
                
                random_questions = []
                while len(random_questions) < tests_count:
                    question=random.choice(questions)
                    while question in random_questions:
                        question=random.choice(questions)
                    random_questions.append(question)
                    StudentQuestions.objects.create(test=test_obj, question=question, created_by=request.user)
                del questions   # delete the list after being used
                del random_questions
            serialized_data = self.list_serializer_class(test_obj, many=False).data

            now=timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
            time_delta = now.minute-test_obj.date_created.minute
            if time_delta < 0:
                time_delta = 60 + time_delta 
            serialized_data.update({'time_limit':60, 'remained_time':60-time_delta})

            return Response(serialized_data, status=200)
        return Response(serializer.errors, status=400)
    


class TestUpdateView(APIView):

    def get_queryset(self):
        return StudentTests.objects.all()

    serializer_class = TestCreateSerializer
    list_serializer_class = TestResultsSerializer
    
    def get(self, request, pk):
        test =  get_object_or_404(StudentTests, pk=pk)
        if test.created_by == request.user or request.user.is_superuser:
            serializer = self.list_serializer_class(test, many=False)
        else:
            return Response({'error':'You cannot get the test because of authorization. It is not yours.'}, status=200)
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        test =  get_object_or_404(StudentTests, pk=pk)
        serializer = self.serializer_class(instance=test, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            finished = request.data.get('finished')
            if finished:
                test.finished = True
                
                test.modified_by = request.user
                test.date_modified = datetime.datetime.now()
                
                test.right_answers = test.questions.filter(student_answer__is_right=True).count()
                print(test.right_answers, test.questions.filter(student_answer__is_right=True).count())
                test.save()
            serializer = self.list_serializer_class(test, many=False)
            print(test.questions.filter(student_answer__is_right=True).count())
            print(test.right_answers, test.questions.count())
            serializer.data.update({'percentage':test.right_answers/test.questions.count()*100})
            return Response({'status':'finished', 'percentage':round(test.right_answers/test.questions.count()*100, ndigits=2)}, status=200)
        return Response(serializer.errors, status=400)
        



class PostStudentAnswer(APIView):
    def get_queryset(self):
        return StudentQuestions.objects.all()

    serializer_class = PostAnswerSerializer
    list_serializer_class = StudentQuestionDetailSerializer
    def get(self, request, pk):
        question = get_object_or_404(StudentQuestions, pk=pk)
        serializer = self.list_serializer_class(question, many=False)
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        question = get_object_or_404(StudentQuestions, pk=pk)
        serializer = self.serializer_class(question, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            student_answer = request.data.get('student_answer')
            question.student_answer_id = student_answer
            question.save()
            return Response({'status':'Answer posted.'}, status=200)
        return Response(serializer.errors, status=200)


class StudentResultsView(APIView):
    def get_queryset(self):
        return StudentTests.objects.all()

    def get(self, request):
        return Response({}, status=200)

    def post(self, request):
        return Response({}, status=200)



###########    OLYMPICS     ##################################################
 
class OlympicsView(APIView):
    """
    This API is only for admin.
    Only Admin can create and see the olympics objects.
    For seeing and creating the olympics objects login as admin and use the key that was sent in the succesfull login response. 
    """
    def get_queryset(self):
        return Olympics.objects.all()
    permission_classes = (IsAdminUser, )
    
    def get_serializer_class(self):
        return OlympicSerializer

    def get(self, request):
        serializer = self.get_serializer_class()(self.get_queryset(), many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=201)


class OlympicsDetailView(APIView):
    """
        This API is only for admin. 
        It is used for seeing, updating and deleting
        any one of available olympics objects.
        Use Token, which is sent in succesfull login response as "key",  in header.
    """
    def get_queryset(self):
        return Olympics.objects.all()
    permission_classes = (IsAdminUser, )
    
    def get_serializer_class(self):
        return OlympicSerializer

    def get(self, request, pk):
        olympic = get_object_or_404(Olympics, pk=pk)
        serializer = self.get_serializer_class()(olympic, many=False)
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        olympic = get_object_or_404(Olympics, pk=pk)
        serializer = self.get_serializer_class()(olympic, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=201)

    def put(self, request, pk):
        olympic = get_object_or_404(Olympics, pk=pk)
        serializer = self.get_serializer_class()(olympic, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=201)

    def delete(self, request, pk):
        olympic = get_object_or_404(Olympics, pk=pk)
        if olympic:
            olympic.delete()
            return Response({'status':'successfully deleted'}, status=200)
        return Response({'detail':'Not Found'}, status=404)


class OlympicResultsView(APIView):

    """
    This API is used for getting the results of the olympics by admin.
    Other users get forbidden status in response.
    Token is required.
    """

    def get_queryset(self, pk=None):
        if pk:
            return OlympicResults.objects.filter(olympics_id=pk)
        return OlympicResults.objects.all()

    permission_classes = (IsAdminUser, )
    
    def get_serializer_class(self, user=None):
        if user and user.is_staff==True:
            return OlympicResultsListSerializer
        return OlympicResultsSerializer

    def get(self, request, pk):
        # pk = request.query_params.get('olympics', None)
        serializer = self.get_serializer_class()(self.get_queryset(pk=pk), many=True)        
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        return Response({}, status=200)

    def delete(self, request, pk):
        return Response({'status':'deleted succesfully.'}, status=200)

    
class OlympicTestCreateView(APIView):
    """
    This API is used by all authorized users.
    POST this attributes:  "subject", "klass", "olympics" and you will get response which include the tests with answers.
    Token is required or you will get the unauthorized status instead of your tests.
    """

    def get_queryset(self):
        return OlympicResults.objects.all()

    serializer_class = OlympicResultsSerializer

    def post(self, request):
        subject_id = request.POST.get('subject', None)
        klass = request.POST.get('klass', None)
        olympics_id = request.POST.get('olympics', None)
        
        olympics = get_object_or_404(Olympics, pk=olympics_id)
        subject = get_object_or_404(Olympics, pk=olympics_id)
        
        student_result_obj = OlympicResults.objects.create(
            olympics=olympics, created_by=request.user
            )
        questions = QuestionModel.objects.filter(klass=klass, subject=subject)
        
        # if not enough tests for the subject?
        questions_count = olympics.subjects.get(subject_id=subject_id).questions_count
        if questions.count() < questions_count:
            return Response({
                'detail':' Sorry! Test questions are not enough.'
                }, status=200)
        
        #else tests are enough, good luck
        student_tests = []
        random_questions = []
        while len(random_questions) < questions_count:
            question=random.choice(questions)
            while question in random_questions:
                question=random.choice(questions)
            random_questions.append(question)
            student_olympic_question = OlympicStudentTests(
                result=student_result_obj,
                question=question,
                created_by=request.user
            )
            student_tests.append(student_olympic_question)
        OlympicStudentTests.objects.bulk_create(student_tests)

        #tests have been created.
        #return student tests
        serializer = self.serializer_class(student_result_obj, many=False)        
        return Response(serializer.data, status=201) 


class OlympicTestDetailView(APIView):
    
    """
    This API is used for GET, PUT, PATCH methods.
    Of course, token is required or you will get unauthorized status.
    """

    def get_queryset(self, pk):
        return OlympicResults.objects.get(pk=pk)
    serializer_class = OlympicResultsSerializer
    def get(self, request, pk):
        olympic_result_obj = get_object_or_404(OlympicResults, pk=pk)
        if not olympic_result_obj:
            return Response({"detail":"Not found"}, status=404)
        if olympic_result_obj.created_by==request.user or request.user.is_staff:
            serializer = self.serializer_class(self.get_queryset(pk=pk), many=False)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk):
        olympic_result_obj = get_object_or_404(OlympicResults, pk=pk)
        serializer = self.serializer_class(olympic_result_obj, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        olympic_result_obj = get_object_or_404(OlympicResults, pk=pk)
        if not olympic_result_obj:
            return Response({"detail":"Not found"}, status=404)
        if request.user.is_staff:
            olympic_result_obj.delete()
            return Response({"detail":"deleted succesfully."}, status=200)
        return Response({"detail":"You haven't this permission to delete the test object."}, status=403)
    
class OlympicStudentAnswerView(APIView):

    """
    This API is used for posting student answers to olympic tests.
    The Allowed methods are GET, PATCH.
    Token is required.
    """

    def get_object(self, pk):
        return get_object_or_404(OlympicStudentTests, pk=pk)
    serializer_class = OlympicStudentTestsSerializer
    
    def get(self, request, pk):
        object = self.get_object(pk=pk)
        serializer = self.serializer_class(object, many=False)
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        object = self.get_object(pk=pk)
        serializer = self.serializer_class(object,data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
                

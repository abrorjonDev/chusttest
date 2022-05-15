from cgi import test
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
import random
import datetime
from django.utils import timezone, timesince

from tests.models import QuestionModel

#local imports
from .models import StudentQuestions, StudentTests
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





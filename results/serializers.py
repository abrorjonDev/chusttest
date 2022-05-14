from rest_framework import serializers
from django.contrib.auth import get_user_model


#local imports 
from .models import StudentQuestions, StudentTests
from tests.serializers import AnswersListSerializer, TestListSerializer, QuestionListSerializer, SubjectSerializer

User = get_user_model()

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','pk')

class PostAnswerSerializer(serializers.ModelSerializer):
    question = QuestionListSerializer(required=False, many=False)
    class Meta:
        model = StudentQuestions
        # fields = "__all__"
        exclude = ('test',)

        extra_kwargs = {
            # 'test':{'read_only':True},
            'question':{'read_only':True}
        }

class StudentQuestionDetailSerializer(serializers.ModelSerializer):
    question = QuestionListSerializer(required=False, many=False)
    subject = SubjectSerializer(required=False, many=False)
    created_by = StudentSerializer(required=False, many=False)
    modified_by = StudentSerializer(required=False, many=False)

    class Meta:
        model = StudentQuestions
        # fields = "__all__"
        exclude = ('test',)

        extra_kwargs = {
            # 'test':{'read_only':True},
            'question':{'read_only':True},
            'created_by':{'read_only':True},
            'modified_by':{'read_only':True},
        }



class TestCreateSerializer(serializers.ModelSerializer):
    questions = PostAnswerSerializer(required=False, many=True)
    # subject = SubjectSerializer(required=False, many=False)
    # created_by = StudentSerializer(required=False, many=False)
    # modified_by = StudentSerializer(required=False, many=False)

    class Meta:
        model = StudentTests
        fields = "__all__"
    
        extra_kwargs = {
            'all_questions':{'read_only':True},
            'created_by':{'read_only':True},
            'modified_by':{'read_only':True},
            'date_created':{'read_only':True},
            'date_modified': {'read_only':True},
            'right_answers': {'read_only':True}
        }

class TestResultsSerializer(serializers.ModelSerializer):
    questions = PostAnswerSerializer(required=False, many=True)
    subject = SubjectSerializer(required=False, many=False)
    created_by = StudentSerializer(required=False, many=False)
    modified_by = StudentSerializer(required=False, many=False)

    class Meta:
        model = StudentTests
        fields = "__all__"
    
        extra_kwargs = {
            'all_questions':{'read_only':True},
            'created_by':{'read_only':True},
            'modified_by':{'read_only':True},
            'date_created':{'read_only':True},
            'date_modified': {'read_only':True},
            'right_answers': {'read_only':True}
        }

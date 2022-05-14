from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

#local imports
from .models import QuestionModel, AnswerModel, Subjects

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = ("id", "name", "image")



class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")

class AnswersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerModel
        fields = ("pk", "answer", "image", )

        extra_kwargs = {}


class AnswerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerModel
        fields = "__all__"

        extra_kwargs = {
            'date_created':{'read_only':True},
            'date_modified':{'read_only':True},
            'created_by':{'read_only':True},
            'modified_by':{'read_only':True},
        }

class QuestionListSerializer(serializers.ModelSerializer):
    qanswers = AnswersListSerializer(required=False, many=True)
    created_by = AdminSerializer(required=False, many=False)
    subject = SubjectSerializer(required=False, many=False)
    class Meta:
        model = QuestionModel
        fields = ('id', 'question', 'image', 'qanswers', 'created_by', 'subject')

class QuestionDetailSerializer(serializers.ModelSerializer):
    qanswers = AnswersListSerializer(required=False, many=True)
    created_by = AdminSerializer(required=False, many=False)
    subject = SubjectSerializer(required=False, many=False)
    class Meta:
        model = QuestionModel
        fields = "__all__"


class TestListSerializer(serializers.ModelSerializer):
    qanswers = AnswersListSerializer(required=False, many=True)
    created_by = AdminSerializer(required=False, many=False)
    class Meta:
        model = QuestionModel
        fields = ("pk", "question", "image", "date_created", "date_modified","created_by", "modified_by", "qanswers")
        extra_kwargs = {
                "date_created": {'read_only':True},
                "date_modified": {'read_only':True},
                "created_by": {'read_only':True},
                "modified_by": {'read_only':True},
            }

class TestCreateSerializer(serializers.ModelSerializer):
    answers = AnswersListSerializer(required=True, many=True)
    class Meta:
        model = QuestionModel
        fields = "__all__"

        extra_kwargs = {
            "date_created": {'read_only':True},
            "date_modified": {'read_only':True},
            "created_by": {'read_only':True},
            "modified_by": {'read_only':True},
        }

    def create(self, attrs):
        answers = attrs.pop('answers')
        question = QuestionModel.objects.create(**attrs, created_by=self.contet['request'].user)
        for answer in answers:
            answer_obj = AnswerModel.objects.create(**answer, question=question)
        return question
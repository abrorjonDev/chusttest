from rest_framework import serializers


#local imports
from .models import QuestionModel, AnswerModel, User


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username","first_name", "last_name")







class AnswersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerModel
        fields = ("pk", "answer", "image", "is_right", "date_created", "date_modified","created_by", "modified_by")

        extra_kwargs = {
            # "is_right": {'write_only':True},
            "date_created": {'read_only':True},
            "date_modified": {'read_only':True},
            "created_by": {'read_only':True},
            "modified_by": {'read_only':True},

        }

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
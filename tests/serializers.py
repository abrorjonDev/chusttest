from xml.dom import ValidationErr
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

class AnswersFullAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerModel
        fields = "__all__"

class AnswersListAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerModel
        fields = ("pk", "answer", "image", "is_right")

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
        fields = ("pk", "question", "subject", "klass", "image", "date_created", "date_modified","created_by", "modified_by", "qanswers")
        extra_kwargs = {
                "date_created": {'read_only':True},
                "date_modified": {'read_only':True},
                "created_by": {'read_only':True},
                "modified_by": {'read_only':True},
            }
    
    def create(self, validated_data):
        qanswers = validated_data.pop("qanswers")
        question = QuestionModel.objects.create(**validated_data, created_by=self.context['request'].user)
        for answer in qanswers:
            AnswerModel.objects.create(**answer, question=question, created_by=self.context['request'].user)
        return question

    def update(self, instance, validated_data):
        instance.question = validated_data.get('question', instance.question)
        instance.subject = validated_data.get('subject', instance.subject)
        instance.klass = validated_data.get('klass', instance.klass)
        instance.modified_by = self.context['request'].user
        instance.save()
        return instance

class TestAdminListSerializer(serializers.ModelSerializer):
    qanswers = AnswersListAdminSerializer(required=False, many=True)
    class Meta:
        model = QuestionModel
        fields = "__all__"

        extra_kwargs = {
            "date_created": {'read_only':True},
            "date_modified": {'read_only':True},
            "created_by": {'read_only':True},
            "modified_by": {'read_only':True},
        }

    def create(self, validated_data):
        # if 'qanswers' not in validated_data.keys():
        #     raise ValidationErr('Answers has not been sent.')
        qanswers = validated_data.pop("qanswers")
        question = QuestionModel.objects.create(**validated_data, created_by=self.context['request'].user)
        for answer in qanswers:
            AnswerModel.objects.create(**answer, question=question, created_by=self.context['request'].user)
        return question

    def update(self, instance, validated_data):
        instance.question = validated_data.get('question', instance.question)
        instance.subject = validated_data.get('subject', instance.subject)
        instance.klass = validated_data.get('klass', instance.klass)
        instance.modified_by = self.context['request'].user
        instance.save()
        return instance


class TestCreateSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=5000)
    q_image = serializers.ImageField(required=False)
    subject = serializers.IntegerField(required=False)
    klass = serializers.CharField(required=False)

    right_answer_1 = serializers.CharField(max_length=5000)
    right_answer_1_image = serializers.ImageField(required=False)

    wrong_answer_2 = serializers.CharField(max_length=5000)
    wrong_answer_2_image = serializers.ImageField(required=False)

    wrong_answer_3 = serializers.CharField(max_length=5000)
    wrong_answer_3_image = serializers.ImageField(required=False)

    wrong_answer_4 = serializers.CharField(max_length=5000)
    wrong_answer_4_image = serializers.ImageField(required=False)

    def create(self, validated_data):
        question = validated_data.get('question', None)
        q_image = validated_data.get('q_image', None)
        subject = validated_data.get('subject', None)
        klass = validated_data.get('klass', None)

        try:
            question = QuestionModel.objects.create(question=question, 
                q_image=q_image, subject_id=subject, 
                klass=klass, 
                created_by=self.context['request'].user
                )
            
            right_answer = AnswerModel.objects.create(answer=validated_data.get('right_answer_1', None),
                image=validated_data.get('right_answer_1_image', None),
                question=question,
                is_right=True,
                created_by=self.context['request'].user
                )

            wrong_answer = AnswerModel.objects.create( 
                answer=validated_data.get('wrong_answer_2', None),
                image=validated_data.get('wrong_answer_2_image', None), 
                question=question, 
                is_right=False, 
                created_by=self.context['request'].user
                )

            wrong_answer = AnswerModel.objects.create( 
                answer=validated_data.get('wrong_answer_3', None), 
                image=validated_data.get('wrong_answer_3_image', None), 
                question=question, 
                is_right=False, 
                created_by=self.context['request'].user)

            wrong_answer = AnswerModel.objects.create( 
                answer=validated_data.get('wrong_answer_4', None), 
                image=validated_data.get('wrong_answer_4_image', None), 
                question=question, 
                is_right=False, created_by=self.context['request'].user
                )
            return question
        except Exception as e:
            raise e

from django.db import models
from django.contrib.auth import get_user_model
from base_model.models import BaseModel

User = get_user_model()
#local imports
from tests.models import QuestionModel, AnswerModel, Subjects

 

# class StatisticsModel(BaseModel):
#     student = models.ForeignKey(User)


class StudentTests(BaseModel):
    CLASSES = (
        ('5', '5-sinf'),
        ('6', '6-sinf'),
        ('7', '7-sinf'),
        ('8', '8-sinf'), 
        ('9', '9-sinf'),
        ('10', '10-sinf'),
        ('11', '11-sinf'),
    )
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    klass = models.CharField(max_length=3, choices=CLASSES, null=True, blank=True)
    finished = models.BooleanField(default=False)
    right_answers = models.IntegerField(default=0)
    @property
    def questions(self):
        return self.questions.all()

    def __str__(self):
        return self.created_by.username

class StudentQuestions(BaseModel):
    test = models.ForeignKey(StudentTests, on_delete=models.CASCADE, related_name="questions")
    question = models.ForeignKey(QuestionModel, on_delete=models.SET_NULL, null=True)
    student_answer = models.ForeignKey(AnswerModel, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.created_by.username

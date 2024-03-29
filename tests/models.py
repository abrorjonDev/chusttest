from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy  as _
import random
User = get_user_model()

#local imports
from base_model.models import BaseModel


def randomize(objects):
    randomized = []
    print(objects)
    if objects.count()<4:
        return objects
    count = random.randint(1, 4)
    if count == 1:
        randomized.update([objects[3], objects[1], objects[0], objects[2]])
    elif count == 1:
        randomized.update([objects[1], objects[3], objects[2], objects[0]])
    elif count == 1:
        randomized.update([objects[3], objects[2], objects[0], objects[1]])
    elif count == 1:
        randomized.update([objects[3], objects[1], objects[2], objects[0]])
    return randomized

class Subjects(BaseModel):
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to="subjects", null=True, blank=True)

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self) -> str:
        return self.name

class QuestionModel(BaseModel):
    CLASSES = (
        ('1', '1-sinf'),
        ('2', '2-sinf'),
        ('3', '3-sinf'),
        ('4', '4-sinf'),
        ('5', '5-sinf'),
        ('6', '6-sinf'),
        ('7', '7-sinf'),
        ('8', '8-sinf'),
        ('9', '9-sinf'),
        ('10', '10-sinf'),
        ('11', '11-sinf'),
    )
    question = models.CharField(max_length=10000, null=True, blank=True)
    image = models.ImageField(upload_to="questions", null=True, blank=True)
    subject = models.ForeignKey(Subjects, on_delete=models.SET_NULL, null=True, blank=True)
    klass = models.CharField(max_length=3, choices=CLASSES, null=True, blank=True)
    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    @property
    def qanswers(self):
        return self.answers.order_by('answer', '-id')
            

    def __str__(self) -> str:
        return self.question or str(self.id)

class AnswerModel(BaseModel):
    answer = models.CharField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to="answers", null=True, blank=True)
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, related_name="answers")
    is_right = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')

    def __str__(self):
        return self.answer or str(self.id)





from django.db import models
from django.contrib.auth import get_user_model
from base_model.models import BaseModel

User = get_user_model()
#local imports
from tests.models import QuestionModel, AnswerModel, Subjects


class StudentTests(BaseModel):
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
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    klass = models.CharField(max_length=3, choices=CLASSES, null=True, blank=True)
    finished = models.BooleanField(default=False)
    right_answers = models.IntegerField(default=0)
    @property
    def questions(self):
        return self.questions.all()

    class Meta:
        verbose_name = "Student Test"
        verbose_name_plural = "Student Tests"
        ordering = ("-id", )

    def __str__(self):
        return self.created_by.username

class StudentQuestions(BaseModel):
    test = models.ForeignKey(StudentTests, on_delete=models.CASCADE, related_name="questions")
    question = models.ForeignKey(QuestionModel, on_delete=models.SET_NULL, null=True)
    student_answer = models.ForeignKey(AnswerModel, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.created_by.username

    class Meta:
        ordering = ('id', )


#######   STATISTICS   ###########################

class StudentResults(BaseModel):
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    percentage = models.FloatField(null=True, blank=True)
    #student --> created_by
    #time ----> date_created, date_modified

    class Meta:
        verbose_name = 'Student Result'
        verbose_name_plural = 'Student Results'
        ordering = ('-pk', )
    def __str__(self) -> str:
        return self.subject.name



class MonthlyStatistics(BaseModel):
    percentage = models.FloatField(null=True, blank=True)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    month = models.CharField(max_length=12)#nw.strftime("%B")
    class Meta:
        verbose_name = 'Monthly Statistics'
        verbose_name_plural = 'Monthly Statistics'
        ordering = ('-pk', )

    def __str__(self) -> str:
        return self.subject.name
        
####### OLYMPICS ##################################

class Olympics(BaseModel):
    title = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="olympics", null=True, blank=True)
    text = models.TextField()
    time_start = models.DateTimeField(null=True, blank=True)
    time_end = models.DateTimeField(null=True, blank=True)
    time_limit = models.FloatField(help_text="limit time in hours", null=True, blank=True)
    avg_result = models.FloatField(help_text="average ball of students", null=True, blank=True)
    class Meta:
        verbose_name = "Olympic"
        verbose_name_plural = "Olympics"
 
    @property
    def subjects(self):
        return self.subjects.all()
 
    @property
    def results(self):
        return self.results.all()

    def __str__(self):
        return self.title

class OlympicsSubjects(BaseModel):
    olympics = models.ForeignKey(Olympics, on_delete=models.SET_NULL, null=True, blank=True, related_name="subjects")
    subject = models.ForeignKey(Subjects, on_delete=models.SET_NULL, null=True, blank=True)
    questions_count = models.IntegerField()
    ball = models.FloatField(default=1.1)

    class Meta:
        verbose_name = "Olympic Subject"
        verbose_name_plural = "Olympic Subjects"

    def __str__(self):
        return self.subject.name

 
class OlympicResults(BaseModel):
    olympics = models.ForeignKey(Olympics, on_delete=models.SET_NULL, null=True, blank=True, related_name="results")
    ball = models.FloatField(null=True, blank=True)
    finished = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Olympic Result"
        verbose_name_plural = "Olympic Results"

    def __str__(self) -> str:
        return self.created_by.full_name

    @property
    def questions(self):
        return self.tests.all()




class OlympicStudentTests(BaseModel):
    result = models.ForeignKey(OlympicResults, on_delete=models.CASCADE, related_name="tests")
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)
    student_answer = models.ForeignKey(AnswerModel, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Olympic Test"
        verbose_name = "Olympic Tests"

    def __str__(self) -> str:
        return self.result.created_by.full_name


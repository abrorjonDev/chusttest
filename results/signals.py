from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from django.utils import timezone

#local imports
from .models import MonthlyStatistics, StudentTests, StudentResults, OlympicResults


@receiver(post_save, sender=StudentTests)
def save_new_percentage_value_to_results_table(sender, instance, **kwargs):
    if instance.finished:
        curr_time = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
        all_tests_answered_by_file = StudentTests.objects.filter(
            created_by=instance.created_by,
            date_created__month=curr_time.month, 
            date_created__year=curr_time.year,
            subject=instance.subject
            )
        percentage = sum((test.right_answers/test.questions.count())*100 for test in all_tests_answered_by_file)/all_tests_answered_by_file.count()

        try:
            result_obj = StudentResults.objects.get(subject=instance.subject, created_by=instance.created_by, date_created__month=curr_time.month, date_created__year=curr_time.year)
            result_obj.percentage = round(percentage, 2)
            result_obj.modified_by = instance.modified_by
            result_obj.save()
        except:
            result_obj = StudentResults.objects.create(subject=instance.subject, created_by=instance.created_by, percentage=round(percentage, 2))
    return instance


@receiver(post_save, sender=StudentResults)
def save_new_percentage_value_to_monthly_model(sender, instance, created, **kwargs):
    curr_time = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
    results = StudentResults.objects.filter(subject=instance.subject, date_created__month=curr_time.month, date_created__year=curr_time.year)
    percentage = sum([res.percentage for res in results])/results.count() if results.count()>0 else 0.0
    try:
        monthly_obj = MonthlyStatistics.objects.get(subject=instance.subject, date_created__month=curr_time.month, date_created__year=curr_time.year)        
    except:
        monthly_obj = MonthlyStatistics.objects.create(subject=instance.subject)
    monthly_obj.percentage = percentage
    monthly_obj.month = curr_time.strftime("%B")
    monthly_obj.save()
    return instance



# @receiver(post_save, sender=OlympicResults)
# def save_student_olympic_result_ball(sender, instance, created, **kwargs):
#     if instance.finished:
#         subjects = instance.olympics.subjects.all()
#         ball = 0.0
#         for subject in subjects:
#             ball += instance.questions.filter(question__subject=subject.subject, student_answer__is_right=True, created_by=instance.created_by).count()*subject.ball
#         instance.ball = ball
#         instance.save()
#     return instance


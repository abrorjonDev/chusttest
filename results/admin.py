from django.contrib import admin

from .models import OlympicResults, OlympicStudentTests, Olympics, OlympicsSubjects, StudentTests, StudentQuestions



@admin.register(StudentTests)
class StudentTestsAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created', 'date_modified', 'created_by', 'modified_by', 'right_answers')
    list_display = ('created_by', 'modified_by')


@admin.register(StudentQuestions)
class StudentQuestionsAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created', 'date_modified', 'created_by', 'modified_by')
    list_display = ('question', 'created_by', 'modified_by')


admin.site.register(OlympicResults)
admin.site.register(Olympics)

admin.site.register(OlympicsSubjects)
admin.site.register(OlympicStudentTests)

from django.contrib import admin

#local imports
from .models import QuestionModel, AnswerModel


class AnswersInline(admin.TabularInline):
    model = AnswerModel
    fields = ('answer', 'image', 'is_right')
    extra = 0

@admin.register(QuestionModel)
class QuestionAdmin(admin.ModelAdmin):

    list_display = ('question', 'id', 'image', 'date_created', 'date_modified')
    search_fields = ('question', 'created_by__username', 'modified_by__username')
    readonly_fields = ('date_created', 'date_modified', 'created_by', 'modified_by')
    fieldsets = (
        (None, {
            'fields':('question', 'image')
        },),
        ('IMPORTANT', {
            'fields':(('created_by', 'date_created'), ('modified_by', 'date_modified'))
        },),
    )

    inlines = [AnswersInline]

    def save_model(self, obj, modeladmin):
        pass



@admin.register(AnswerModel)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'image', 'is_right', 'date_created',)
    readonly_fields = ('date_created', 'date_modified', 'created_by', 'modified_by')
    search_fields = ('question', 'answer', 'created_by', 'modified_by')

    fieldsets = (
        (None, {
            'fields':('answer', 'image', 'question', 'is_right'),
        },),
         ('IMPORTANT', {
            'fields':(('created_by', 'date_created'), ('modified_by', 'date_modified'))
        },),
    )
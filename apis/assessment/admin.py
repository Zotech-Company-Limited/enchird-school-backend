from django.contrib import admin
from .models import Assessment, Question, Choice



@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('assessment_id', 'title', 'description', 'assessment_type', 'course', 'instructor', 'created_at')
    search_fields = ('assessment_id', 'title')
    list_filter = ('assessment_type', 'course', 'instructor', 'created_at')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('assessment', 'text', 'created_at')
    search_fields = ('assessment__title', 'text')
    list_filter = ('assessment__title', 'created_at')


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct')
    search_fields = ('question__text', 'text')
    list_filter = ('question__text', 'is_correct')
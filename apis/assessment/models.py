from django.db import models
from django.contrib import admin
from apis.users.models import User
from django.dispatch import receiver
from apis.courses.models import Course
from django.db.models.signals import post_save



# Register your models here.

class Assessment(models.Model):

    TEXT_TYPE = 'text'
    MIXED_TYPE = 'mixed'
    MULTIPLE_CHOICE_TYPE = 'mcq'

    ASSESSMENT_TYPE_CHOICES = [
        (TEXT_TYPE, 'Text'),
        (MIXED_TYPE, 'Mixed'),
        (MULTIPLE_CHOICE_TYPE, 'Multiple Choice'),
    ]

    assessment_id = models.CharField(max_length=255, blank=False, null=False, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPE_CHOICES, default=MULTIPLE_CHOICE_TYPE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=Assessment, dispatch_uid="update_assessment_id")
def update_assessment_id(instance, **kwargs):
    if not instance.assessment_id:
        instance.assessment_id = 'ASM_' + str(instance.id).zfill(8)
        instance.save()


class Question(models.Model):

    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    image = models.ImageField(upload_to='question_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" Question for Assessment: {self.assessment.title}"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Choice: {self.text} for Question: {self.question.text}"



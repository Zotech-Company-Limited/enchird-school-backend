from django.db import models
from apis.users.models import User
from django.dispatch import receiver
from apis.teachers.models import Teacher
from django.db.models.signals import post_save


# Create your models here.
class Course(models.Model):

    # Course Status
    COURSE_STATUS_CHOICES = [
        ('open', 'Open for Enrollment'),
        ('closed', 'Closed'),
        ('canceled', 'Canceled'),
    ]

    course_id = models.CharField(max_length=255, blank=False, null=False, unique=True)
    course_title = models.CharField(max_length=100, blank=False,null=False, unique=True)
    course_code = models.CharField(max_length=10, blank=False,null=False, unique=True)
    description = models.TextField(max_length=255, null=True, blank=True)
    prerequisites = models.CharField(max_length=10, blank=True, null=True)
    instructors = models.ManyToManyField(
        User,
        related_name='instructed_courses'
    )
    # Schedule and Location
    class_schedule = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    # Materials and Objectives
    course_materials = models.TextField(blank=True, null=True)
    learning_objectives = models.TextField(blank=True, null=True)

    # Assessment and Grading
    assessment_and_grading = models.TextField(blank=True, null=True)
    office_hours = models.CharField(max_length=255, blank=True, null=True)
    term = models.CharField(max_length=50, blank=True, null=True)
    credits = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    course_status = models.CharField(max_length=20, choices=COURSE_STATUS_CHOICES, default='Open')

    created_at = models.DateTimeField(
        db_column="creation_date",
        auto_now_add=True
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True
    )
    
    def __str__(self):
        return self.course_title

    class Meta:
        db_table = "course"


@receiver(post_save, sender=Course, dispatch_uid="update_course_id")
def update_course_id(instance, **kwargs):
    if not instance.course_id:
        instance.course_id = 'COUR_' + str(instance.id).zfill(8)
        instance.save()
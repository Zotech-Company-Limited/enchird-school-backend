import datetime
import hashlib
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from apis.users.models import User



# Create your models here.

class Teacher(models.Model):
    """Docstring for class."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=255, blank=False, null=False, unique=True)
    highest_degree = models.CharField(max_length=100, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        db_column="creation_date",
        auto_now_add=True
    )
    
    def __str__(self):
        return self.teacher_id

    class Meta:
        db_table = "teachers"


@receiver(post_save, sender=Teacher, dispatch_uid="update_teacher_id")
def update_teacher_id(instance, **kwargs):
    if not instance.teacher_id:
        instance.teacher_id = 'TCH_' + str(instance.id).zfill(8)
        instance.save()
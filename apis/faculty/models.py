from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from apis.users.models import User

# Create your models here.

class Faculty(models.Model):

    faculty_id = models.CharField(max_length=255, blank=False, null=False, unique=True)
    name = models.CharField(max_length=100, blank=False,null=False, unique=True)
    abbrev = models.CharField(max_length=10, blank=False, null=False)
    is_deleted = models.BooleanField(default=False)
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
        return self.faculty_id

    class Meta:
        db_table = "faculty"


@receiver(post_save, sender=Faculty, dispatch_uid="update_faculty_id")
def update_faculty_id(instance, **kwargs):
    if not instance.faculty_id:
        instance.faculty_id = 'FAC_' + str(instance.id).zfill(8)
        instance.save()


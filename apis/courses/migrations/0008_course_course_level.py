# Generated by Django 4.2.7 on 2024-01-05 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_remove_course_instructors_remove_course_office_hours_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_level',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]

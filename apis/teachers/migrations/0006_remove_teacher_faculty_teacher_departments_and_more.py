# Generated by Django 4.2.7 on 2024-01-10 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0008_alter_faculty_levels'),
        ('teachers', '0005_alter_teacher_courses'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='faculty',
        ),
        migrations.AddField(
            model_name='teacher',
            name='departments',
            field=models.ManyToManyField(blank=True, related_name='teachers', to='faculty.department'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='faculties',
            field=models.ManyToManyField(blank=True, related_name='teachers', to='faculty.faculty'),
        ),
    ]
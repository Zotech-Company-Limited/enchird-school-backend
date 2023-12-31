# Generated by Django 4.2.7 on 2023-11-16 22:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=255, unique=True)),
                ('course_title', models.CharField(max_length=100, unique=True)),
                ('course_code', models.CharField(max_length=10, unique=True)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('prerequisites', models.CharField(blank=True, max_length=10, null=True)),
                ('class_schedule', models.CharField(blank=True, max_length=255, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('course_materials', models.TextField(blank=True, null=True)),
                ('learning_objectives', models.TextField(blank=True, null=True)),
                ('assessment_and_grading', models.TextField(blank=True, null=True)),
                ('office_hours', models.CharField(blank=True, max_length=255, null=True)),
                ('term', models.CharField(blank=True, max_length=50, null=True)),
                ('credits', models.PositiveIntegerField(default=0)),
                ('is_deleted', models.BooleanField(default=False)),
                ('course_status', models.CharField(choices=[('Open', 'Open for Enrollment'), ('Closed', 'Closed'), ('Canceled', 'Canceled'), ('Waitlisted', 'Waitlisted')], default='Open', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='creation_date')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('instructor', models.ManyToManyField(related_name='instructed_courses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'course',
            },
        ),
    ]

# Generated by Django 4.2.7 on 2024-01-09 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_course_course_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_status',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
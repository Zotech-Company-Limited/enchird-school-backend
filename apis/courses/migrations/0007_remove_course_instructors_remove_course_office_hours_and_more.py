# Generated by Django 4.2.7 on 2024-01-05 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0005_alter_faculty_member_department'),
        ('courses', '0006_remove_course_course_materials_coursematerial_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='instructors',
        ),
        migrations.RemoveField(
            model_name='course',
            name='office_hours',
        ),
        migrations.RemoveField(
            model_name='course',
            name='prerequisites',
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='course_department', to='faculty.department'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='faculty',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='course_faculty', to='faculty.faculty'),
            preserve_default=False,
        ),
    ]
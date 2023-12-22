# Generated by Django 4.2.7 on 2023-12-20 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_alter_user_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_faculty_member',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('superadmin', 'Superadmin'), ('student', 'Student'), ('faculty', 'Faculty_Member'), ('teacher', 'Teacher')], default='student', max_length=10),
        ),
    ]

# Generated by Django 4.2.6 on 2023-10-26 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_remove_student_activate_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 4.2.7 on 2024-01-29 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0003_remove_chatgroup_course_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupmessage',
            name='sender',
            field=models.CharField(max_length=255),
        ),
    ]

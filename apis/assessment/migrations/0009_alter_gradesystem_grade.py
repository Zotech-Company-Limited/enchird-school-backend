# Generated by Django 4.2.7 on 2023-12-27 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0008_gradesystem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gradesystem',
            name='grade',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]

# Generated by Django 4.2.7 on 2023-12-08 01:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0005_studentresponse_recorded_at'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='assessment',
            table='assessments',
        ),
    ]
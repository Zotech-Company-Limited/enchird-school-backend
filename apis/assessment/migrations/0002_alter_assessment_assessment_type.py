# Generated by Django 4.2.7 on 2023-12-05 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='assessment_type',
            field=models.CharField(choices=[('text', 'Text'), ('mixed', 'Mixed'), ('mcq', 'Multiple Choice')], default='mcq', max_length=20),
        ),
    ]
# Generated by Django 4.2.7 on 2024-01-06 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0005_alter_faculty_member_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='about',
            field=models.CharField(blank=True, max_length=244, null=True),
        ),
        migrations.AddField(
            model_name='department',
            name='description',
            field=models.CharField(blank=True, max_length=244, null=True),
        ),
        migrations.AddField(
            model_name='faculty',
            name='about',
            field=models.CharField(blank=True, max_length=244, null=True),
        ),
        migrations.AddField(
            model_name='faculty',
            name='description',
            field=models.CharField(blank=True, max_length=244, null=True),
        ),
    ]
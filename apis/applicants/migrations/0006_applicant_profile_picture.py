# Generated by Django 4.2.7 on 2023-12-15 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0005_alter_achievementdocument_document_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='profile_picture',
            field=models.CharField(default='d', max_length=255),
            preserve_default=False,
        ),
    ]
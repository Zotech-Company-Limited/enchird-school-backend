# Generated by Django 4.2.7 on 2023-12-14 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0003_alter_achievementdocument_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievementdocument',
            name='document',
            field=models.FileField(upload_to='achievement_documents/'),
        ),
    ]

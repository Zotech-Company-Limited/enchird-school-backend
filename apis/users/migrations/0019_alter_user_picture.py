# Generated by Django 4.2.7 on 2023-11-19 20:07

import apis.users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(default=None, null=True, upload_to=apis.users.models.User.user_directory_path),
        ),
    ]
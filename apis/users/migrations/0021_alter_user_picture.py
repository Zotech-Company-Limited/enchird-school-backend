# Generated by Django 4.2.7 on 2023-12-15 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.CharField(max_length=255),
        ),
    ]
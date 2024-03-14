# Generated by Django 4.2.7 on 2024-03-14 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0017_librarybook'),
        ('messaging', '0006_zoommeeting'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatgroup',
            name='course',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='chat_groups', to='courses.course'),
            preserve_default=False,
        ),
    ]

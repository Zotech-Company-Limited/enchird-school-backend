# Generated by Django 4.2.7 on 2024-02-07 03:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('faculty', '0009_department_abbrev'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('position_type', models.CharField(choices=[('remote', 'Remote'), ('on_site', 'On Site'), ('hybrid', 'Hybrid')], max_length=20)),
                ('employment_type', models.CharField(choices=[('part_time', 'Part-Time'), ('contract', 'Contract'), ('full_time', 'Full-Time')], max_length=20)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='opportunity_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'opportunities',
            },
        ),
    ]

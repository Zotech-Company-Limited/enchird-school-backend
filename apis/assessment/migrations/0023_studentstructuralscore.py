# Generated by Django 4.2.7 on 2024-03-22 19:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assessment', '0022_delete_studentquestionscore'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentStructuralScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.CharField(max_length=255)),
                ('is_graded', models.BooleanField(default=False)),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessment.assessment')),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='assessment.question')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
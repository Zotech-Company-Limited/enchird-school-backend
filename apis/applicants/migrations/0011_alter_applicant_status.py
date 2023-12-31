# Generated by Django 4.2.7 on 2023-12-18 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0010_remove_applicant_is_selected_applicant_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='status',
            field=models.CharField(choices=[('accepted', 'Accepted'), ('rejected', 'Rejected'), ('pending', 'Pending')], default='pending', max_length=8),
        ),
    ]

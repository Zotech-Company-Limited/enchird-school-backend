# Generated by Django 4.2.7 on 2024-03-14 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_userpayment_paypal_checkout_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpayment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('successful', 'Successful'), ('failed', 'Failed')], default='pending', max_length=20),
        ),
    ]

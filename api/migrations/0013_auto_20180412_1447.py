# Generated by Django 2.0.1 on 2018-04-12 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20180412_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetlog',
            name='log_type',
            field=models.CharField(choices=[('Checkin', 'Checkin'), ('Checkout', 'Checkout')], max_length=10),
        ),
    ]

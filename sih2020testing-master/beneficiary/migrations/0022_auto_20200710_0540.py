# Generated by Django 3.0.7 on 2020-07-10 05:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiary', '0021_remove_userappointments_apuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbmi',
            name='bmdate',
            field=models.DateField(default=datetime.date(2020, 7, 10)),
        ),
    ]
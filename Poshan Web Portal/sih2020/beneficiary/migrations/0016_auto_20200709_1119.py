# Generated by Django 3.0.5 on 2020-07-09 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiary', '0015_auto_20200709_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userappointments',
            name='apstatus',
            field=models.CharField(default=None, max_length=10),
        ),
    ]

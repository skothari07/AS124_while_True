# Generated by Django 3.0.7 on 2020-07-26 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiary', '0041_auto_20200726_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='userappointments',
            name='aptype',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]

# Generated by Django 3.0.7 on 2020-07-26 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiary', '0040_auto_20200726_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userappointments',
            name='apstatus',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]

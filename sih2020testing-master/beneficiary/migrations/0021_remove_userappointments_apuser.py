# Generated by Django 3.0.5 on 2020-07-09 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiary', '0020_auto_20200709_1634'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userappointments',
            name='apuser',
        ),
    ]
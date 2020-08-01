# Generated by Django 3.0.5 on 2020-07-09 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiary', '0013_userappointments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userappointments',
            name='apid',
        ),
        migrations.AddField(
            model_name='userappointments',
            name='apuid',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='userappointments',
            name='apdate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='userappointments',
            name='apno',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='userappointments',
            name='apstatus',
            field=models.CharField(max_length=10, null=True),
        ),
    ]

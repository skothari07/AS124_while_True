# Generated by Django 3.0.5 on 2020-07-11 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiary', '0025_userbmi_bmworker'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userappointments',
            old_name='apuid',
            new_name='u_user_id',
        ),
        migrations.RenameField(
            model_name='userbmi',
            old_name='bmid',
            new_name='u_user_id',
        ),
        migrations.RemoveField(
            model_name='userbmi',
            name='bmuser',
        ),
    ]

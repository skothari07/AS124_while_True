# Generated by Django 3.0.5 on 2020-07-03 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0006_worker_register_hw_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worker_register',
            name='hw_password',
        ),
    ]
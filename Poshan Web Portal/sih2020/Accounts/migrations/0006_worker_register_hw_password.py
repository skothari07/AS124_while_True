# Generated by Django 3.0.5 on 2020-07-03 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0005_remove_worker_register_hw_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker_register',
            name='hw_password',
            field=models.CharField(default=None, max_length=20),
        ),
    ]

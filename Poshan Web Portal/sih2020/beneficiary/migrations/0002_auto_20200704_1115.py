# Generated by Django 3.0.5 on 2020-07-04 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiary_register',
            name='u_verified',
            field=models.CharField(default=None, max_length=13, null=True),
        ),
    ]

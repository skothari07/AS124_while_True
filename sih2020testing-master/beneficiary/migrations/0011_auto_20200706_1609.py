# Generated by Django 3.0.5 on 2020-07-06 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiary', '0010_beneficiary_register_u_addr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiary_register',
            name='u_status',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]

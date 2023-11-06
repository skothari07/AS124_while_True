# Generated by Django 3.0.5 on 2020-07-04 06:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('beneficiary', '0006_auto_20200704_1212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='beneficiary_register',
            name='u_status',
        ),
        migrations.RemoveField(
            model_name='beneficiary_register',
            name='u_verified',
        ),
        migrations.AlterField(
            model_name='beneficiary_register',
            name='u_user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
# Generated by Django 3.0.5 on 2020-07-04 05:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='beneficiary_register',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('u_fname', models.CharField(default=None, max_length=30)),
                ('u_sname', models.CharField(default=None, max_length=30)),
                ('u_adhar', models.CharField(default=None, max_length=12)),
                ('u_pincode', models.CharField(default=None, max_length=6)),
                ('u_district', models.CharField(default=None, max_length=20)),
                ('u_phno', models.CharField(default=None, max_length=13)),
                ('u_status', models.BooleanField(null=True)),
                ('u_verified', models.CharField(default=None, max_length=13)),
                ('u_user', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
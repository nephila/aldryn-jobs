# Generated by Django 2.2.12 on 2020-12-04 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_jobs', '0008_auto_20201202_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='mobile_phone',
            field=models.CharField(default='', max_length=20, verbose_name='phone number'),
        ),
    ]
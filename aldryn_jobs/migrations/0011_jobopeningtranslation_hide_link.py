# Generated by Django 2.2.12 on 2021-04-14 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_jobs', '0010_auto_20201209_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobopeningtranslation',
            name='hide_link',
            field=models.BooleanField(default=False, verbose_name='hide link in jobs list'),
        ),
    ]

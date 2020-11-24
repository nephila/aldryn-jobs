# Generated by Django 2.2.12 on 2020-11-24 09:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_jobs', '0006_auto_20201020_1454'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobapplication',
            name='abc_analysis_explaination',
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='abc_analysis_explanation',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='abc analysis explanation'),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='notice_period_other',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='other (notice period)'),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='how_hear_about_us',
            field=models.CharField(blank=True, choices=[('', 'Please select'), ('linkedin', 'LinkedIn'), ('rahn website', 'RAHN Website'), ('other', 'Other (please specify) ')], max_length=12, null=True, verbose_name='how did you hear about us?'),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='mobile_phone',
            field=models.CharField(default='', max_length=20, verbose_name='mobile number'),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='notice_period',
            field=models.CharField(blank=True, choices=[('', 'Please select'), ('1 month', '1 month'), ('2 months', '2 months'), ('3 months', '3 months'), ('6 months', '6 months'), ('none', 'None'), ('other', 'Other (please specify)')], max_length=10, null=True, verbose_name='notice period'),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='valid_work_permit',
            field=models.CharField(blank=True, choices=[('', 'Please select'), ('yes', 'Yes'), ('no', 'No')], max_length=3, null=True, verbose_name='valid work permit'),
        ),
        migrations.AlterField(
            model_name='jobopening',
            name='responsibles',
            field=models.ManyToManyField(blank=True, limit_choices_to={'groups__name': 'Rahn HR Responsibles'}, to=settings.AUTH_USER_MODEL, verbose_name='responsibles'),
        ),
    ]

# Generated by Django 2.1.4 on 2020-08-31 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iterable',
            name='end_time',
            field=models.DateField(default='1970-01-01', verbose_name='结束时间'),
        ),
        migrations.AlterField(
            model_name='iterable',
            name='start_time',
            field=models.DateField(default='1970-01-01', verbose_name='开始时间'),
        ),
        migrations.AlterField(
            model_name='onlinebug',
            name='end_time',
            field=models.DateField(default='1970-01-01', verbose_name='结束时间'),
        ),
        migrations.AlterField(
            model_name='onlinebug',
            name='start_time',
            field=models.DateField(default='1970-01-01', verbose_name='开始时间'),
        ),
    ]

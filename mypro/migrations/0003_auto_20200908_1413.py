# Generated by Django 2.1.4 on 2020-09-08 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypro', '0002_auto_20200831_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcase',
            name='main_tasks',
            field=models.CharField(max_length=200),
        ),
    ]
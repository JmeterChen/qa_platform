# Generated by Django 3.0.4 on 2020-08-25 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tapd', '0002_auto_20200612_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='projecttoken',
            name='is_delete',
            field=models.IntegerField(choices=[(0, '否'), (1, '是')], default=0, verbose_name='删除状态'),
        ),
    ]

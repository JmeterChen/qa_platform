# Generated by Django 2.1.4 on 2020-08-18 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mypro', '0003_auto_20200818_1407'),
    ]

    operations = [
        migrations.RenameField(
            model_name='services',
            old_name='test_user',
            new_name='test_user_id',
        ),
    ]

# Generated by Django 2.1.4 on 2020-08-17 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testcase', '0003_book'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Book',
        ),
        migrations.DeleteModel(
            name='Case',
        ),
    ]
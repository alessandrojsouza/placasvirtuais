# Generated by Django 3.1.4 on 2021-01-29 01:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_auto_20210128_2200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='campus',
        ),
    ]

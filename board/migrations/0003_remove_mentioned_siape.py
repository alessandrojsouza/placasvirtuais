# Generated by Django 3.1.4 on 2021-01-31 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_auto_20210130_1211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mentioned',
            name='siape',
        ),
    ]

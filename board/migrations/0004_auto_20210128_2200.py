# Generated by Django 3.1.4 on 2021-01-29 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_auto_20210125_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='graduation_date',
            field=models.DateField(verbose_name='Data da formatura'),
        ),
    ]

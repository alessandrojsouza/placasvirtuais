# Generated by Django 3.1.4 on 2021-06-21 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210510_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='campus',
            field=models.TextField(blank=True, null=True, verbose_name='Cmapus'),
        ),
    ]

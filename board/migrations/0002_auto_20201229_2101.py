# Generated by Django 3.1.4 on 2020-12-30 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='photo',
            field=models.ImageField(upload_to='boards', verbose_name='Imagem'),
        ),
    ]

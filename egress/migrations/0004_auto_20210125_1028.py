# Generated by Django 3.1.4 on 2021-01-25 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('egress', '0003_auto_20210125_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='egress',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='egress/', verbose_name='Imagem'),
        ),
    ]
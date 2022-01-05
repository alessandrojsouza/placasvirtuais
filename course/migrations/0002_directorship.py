# Generated by Django 3.1.4 on 2021-12-28 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Directorship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=300, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Diretoria',
                'verbose_name_plural': 'Diretorias',
            },
        ),
    ]
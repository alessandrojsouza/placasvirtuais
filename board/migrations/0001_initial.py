# Generated by Django 2.1.5 on 2020-12-30 01:00

import board.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0001_initial'),
        ('mentioned', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=300, verbose_name='Nome')),
                ('photo', models.ImageField(upload_to='boards', verbose_name='Imagem')),
                ('message', models.TextField(blank=True, null=True, verbose_name='Mensagem')),
                ('year_graduation', models.IntegerField(default=board.models.current_year, verbose_name='Ano do período')),
                ('graduation_date', models.DateTimeField(verbose_name='Data da formatura')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course')),
                ('mentioned', models.ManyToManyField(to='mentioned.Mentioned')),
            ],
            options={
                'verbose_name': 'Board',
                'verbose_name_plural': 'Boards',
            },
        ),
    ]

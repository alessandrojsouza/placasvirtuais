# Generated by Django 3.1.4 on 2020-12-30 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Egress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=300, verbose_name='Nome')),
                ('enrollment', models.CharField(max_length=300, verbose_name='Matricula')),
                ('photo', models.ImageField(upload_to='egress', verbose_name='Imagem')),
                ('lattes', models.CharField(max_length=300, verbose_name='Lattes')),
                ('email', models.CharField(max_length=300, verbose_name='Email')),
                ('social_network', models.CharField(max_length=300, verbose_name='Rede social')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.board')),
            ],
            options={
                'verbose_name': 'Egresso',
                'verbose_name_plural': 'Egressos',
            },
        ),
    ]

# Generated by Django 3.1.4 on 2021-03-27 22:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Livro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50, unique=True)),
                ('nota_media', models.DecimalField(blank=True, decimal_places=1, max_digits=3)),
                ('num_paginas', models.IntegerField()),
                ('data_publicacao', models.DateField()),
                ('total_de_notas', models.IntegerField()),
            ],
            options={
                'ordering': ['titulo'],
            },
        ),
        migrations.CreateModel(
            name='UsuarioLivro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('livro_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leitor', to='livros.livro')),
                ('usuario_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='livro_usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('livro_id', 'usuario_id')},
            },
        ),
    ]

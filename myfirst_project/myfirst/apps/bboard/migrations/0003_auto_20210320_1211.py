# Generated by Django 3.1.7 on 2021-03-20 07:11

import bboard.utilites
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0002_auto_20210318_0554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.CreateModel(
            name='Bb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='Товар')),
                ('content', models.TextField(verbose_name='Oпиcaниe')),
                ('price', models.FloatField(default=0, verbose_name='Цeнa')),
                ('contacts', models.TextField(verbose_name='Koнтaкты')),
                ('image', models.ImageField(blank=True, upload_to=bboard.utilites.get_timestamp_path, verbose_name='Изображение')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='Выводить в списке?')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Aвтop объявления')),
                ('rubric', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bboard.subrubric', verbose_name='Рубрика')),
            ],
            options={
                'verbose_name': 'Объявлние',
                'verbose_name_plural': 'Объявлния',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AdditionalImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=bboard.utilites.get_timestamp_path, verbose_name='Изображение')),
                ('bb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bboard.bb', verbose_name='Объявление')),
            ],
            options={
                'verbose_name': 'Дополнительная иллюстрация',
                'verbose_name_plural': 'Дополнительные иллюстрации',
            },
        ),
    ]
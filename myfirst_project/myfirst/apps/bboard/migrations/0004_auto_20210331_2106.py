# Generated by Django 3.1.7 on 2021-03-31 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0003_auto_20210320_1211'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bb',
            options={'ordering': ['-created_at'], 'verbose_name': 'Объявление', 'verbose_name_plural': 'Объявления'},
        ),
        migrations.CreateModel(
            name='Comment_bb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=30, verbose_name='Автор')),
                ('content', models.TextField(verbose_name='Tекст комментария')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')),
                ('bb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bboard.bb', verbose_name='Объявление')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ['created_at'],
            },
        ),
    ]

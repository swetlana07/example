# Generated by Django 3.1.7 on 2021-03-31 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0004_auto_20210331_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment_bb',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, verbose_name='Выводить на экран?'),
        ),
    ]
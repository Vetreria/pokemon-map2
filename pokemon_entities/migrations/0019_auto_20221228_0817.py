# Generated by Django 3.1.14 on 2022-12-28 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0018_auto_20221228_0720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='title_ru',
            field=models.CharField(max_length=200, verbose_name='Название по-русски'),
        ),
        migrations.AlterField(
            model_name='pokemonelement',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Название по-русски'),
        ),
    ]
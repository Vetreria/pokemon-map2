# Generated by Django 3.1.14 on 2022-12-22 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0005_auto_20221222_0435'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemonentity',
            name='level',
            field=models.IntegerField(null=True),
        ),
    ]
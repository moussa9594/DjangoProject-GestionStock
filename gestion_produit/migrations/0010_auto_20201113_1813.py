# Generated by Django 3.1.2 on 2020-11-13 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_produit', '0009_essaiimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='prix_u',
            field=models.BigIntegerField(),
        ),
    ]

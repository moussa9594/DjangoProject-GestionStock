# Generated by Django 3.1.2 on 2020-11-18 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_commande', '0002_commande_etat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lignecommande',
            name='client',
        ),
        migrations.AddField(
            model_name='commande',
            name='client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestion_commande.client'),
        ),
    ]

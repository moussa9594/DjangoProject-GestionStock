# Generated by Django 3.1.2 on 2020-11-14 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gestion_produit', '0010_auto_20201113_1813'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prenom', models.CharField(max_length=100)),
                ('nom', models.CharField(max_length=100)),
                ('sexe', models.CharField(choices=[('Masculin', 'Masculin'), ('Feminin', 'Feminin')], default='Masculin', max_length=10)),
                ('telephone', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('login', models.CharField(default='', max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('adresse', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_commande', models.DateTimeField(auto_now=True)),
                ('nbre_produit', models.IntegerField()),
                ('prix_total', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LigneCommande',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.PositiveSmallIntegerField()),
                ('sous_total', models.BigIntegerField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_commande.client')),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_commande.commande')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_produit.produit')),
            ],
        ),
    ]

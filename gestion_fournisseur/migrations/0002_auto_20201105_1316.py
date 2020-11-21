# Generated by Django 3.1.2 on 2020-11-05 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_fournisseur', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AjoutProd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=100)),
                ('quantite', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='fournisseur',
            name='telephone',
            field=models.CharField(max_length=9),
        ),
    ]
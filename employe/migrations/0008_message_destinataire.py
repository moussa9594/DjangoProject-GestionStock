# Generated by Django 3.1.2 on 2020-11-10 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employe', '0007_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='destinataire',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]

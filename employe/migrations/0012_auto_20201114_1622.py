# Generated by Django 3.1.2 on 2020-11-14 16:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employe', '0011_auto_20201113_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateField(default=datetime.date(2020, 11, 14)),
        ),
    ]

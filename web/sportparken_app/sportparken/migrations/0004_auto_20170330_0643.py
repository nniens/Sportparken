# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-30 06:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportparken', '0003_huurder_sport'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ondergrond',
            fields=[
                ('tid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, null=True)),
            ],
            options={
                'db_table': 'ondergrond_type',
            },
        ),
        migrations.RemoveField(
            model_name='sportparkobjectgeometry',
            name='objectOndergrond',
        ),
    ]
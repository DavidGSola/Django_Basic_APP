# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bares',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('direccion', models.CharField(max_length=200)),
                ('fecha_visita', models.DateTimeField(verbose_name=b'Fecha visita')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tapas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tapa', models.CharField(max_length=200)),
                ('votos', models.IntegerField(default=0)),
                ('bar', models.ForeignKey(to='bares.Bares')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

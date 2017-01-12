# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('street', models.CharField(max_length=64)),
                ('city', models.CharField(max_length=64)),
                ('state', models.CharField(max_length=2)),
                ('zip_code', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('address', models.CharField(blank=True, null=True, max_length=100)),
                ('a_time', models.FloatField(blank=True, null=True)),
                ('b_time', models.FloatField(blank=True, null=True)),
                ('latlng', models.CharField(blank=True, null=True, max_length=64)),
                ('name', models.CharField(blank=True, null=True, max_length=64)),
                ('place_id', models.CharField(blank=True, null=True, max_length=64)),
                ('score', models.FloatField(blank=True, null=True)),
                ('avg_time', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('business_type', models.CharField(choices=[('cafe', 'Cafe'), ('bar', 'Bar'), ('restaurant', 'Restaurant'), ('book_store', 'Book Store'), ('gas_station', 'Gas Station'), ('library', 'Library')], blank=True, null=True, max_length=64)),
                ('trip_id', models.CharField(blank=True, null=True, max_length=100)),
                ('destinations', models.ManyToManyField(blank=True, to='meethalfway.Destination')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('transit_mode', models.CharField(choices=[('walking', 'Walking'), ('transit', 'Public Transit'), ('driving', 'Driving'), ('bicycling', 'Bicycling')], max_length=70)),
                ('starting_location', models.ForeignKey(to='meethalfway.Address', blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='meeting',
            name='participant_one',
            field=models.ForeignKey(related_name='participant_one', to='meethalfway.Participant', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='participant_two',
            field=models.ForeignKey(related_name='participant_two', to='meethalfway.Participant', blank=True, null=True),
        ),
    ]

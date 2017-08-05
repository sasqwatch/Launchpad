# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-04 15:17
from __future__ import unicode_literals

import dashboard.models.client
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(db_index=True, default=dashboard.models.client._make_client_id, editable=False, max_length=4, unique=True)),
                ('title', models.CharField(blank=True, max_length=128, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_connected', models.DateTimeField(null=True)),
                ('date_disconnected', models.DateTimeField(null=True)),
                ('platform', models.CharField(choices=[('windows', 'Windows')], max_length=8)),
                ('cpu', models.CharField(choices=[('x86', 'x86'), ('x64', 'x64')], max_length=8)),
                ('loader', models.CharField(choices=[('ps1', 'ps1')], max_length=8)),
                ('protocol', models.CharField(choices=[('ws', 'ws'), ('wss', 'wss')], max_length=8)),
                ('method', models.CharField(choices=[('connect', 'Connect'), ('bind', 'Bind')], max_length=8)),
            ],
        ),
    ]
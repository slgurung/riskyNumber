# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-19 14:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Filling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form', models.CharField(max_length=50)),
                ('documentUrl', models.URLField()),
                ('description', models.TextField(null=True)),
                ('fillingDate', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('ticker', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('cik', models.CharField(default='', max_length=20)),
                ('name', models.CharField(default='', max_length=100)),
                ('sector', models.CharField(default='', max_length=100)),
                ('industry', models.CharField(default='', max_length=100)),
                ('exchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riskyNumber.Exchange')),
            ],
        ),
        migrations.CreateModel(
            name='Trending',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10)),
                ('updown', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website', models.URLField(blank=True)),
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='filling',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riskyNumber.Stock'),
        ),
    ]
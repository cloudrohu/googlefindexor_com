# Generated by Django 5.0.1 on 2024-08-23 04:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('response', '0001_initial'),
        ('utility', '0004_city_locality'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='utility.city'),
        ),
        migrations.AddField(
            model_name='response',
            name='locality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='utility.locality'),
        ),
    ]
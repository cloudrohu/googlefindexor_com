# Generated by Django 5.0.1 on 2024-06-08 04:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_alter_approx_category_alter_approx_city_and_more'),
        ('utility', '0002_googlemap_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='googlemap_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='utility.googlemap_status'),
        ),
    ]

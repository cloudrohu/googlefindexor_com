# Generated by Django 5.0.1 on 2024-11-10 10:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0006_company_about'),
        ('visit', '0002_alter_today_visit_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='today_visit',
            name='title',
        ),
        migrations.AddField(
            model_name='today_visit',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business.company'),
        ),
    ]

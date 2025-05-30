# Generated by Django 5.0.1 on 2025-04-06 11:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0005_meeting_followup_type'),
        ('visit', '0008_alter_visit_type_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='today_visit',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='utility.city'),
        ),
        migrations.AlterField(
            model_name='today_visit',
            name='locality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='utility.locality'),
        ),
    ]

# Generated by Django 5.0.1 on 2025-04-06 11:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0009_company_call_comment_company_followup_meeting'),
        ('utility', '0005_meeting_followup_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='locality',
            name='city',
        ),
        migrations.AlterField(
            model_name='company',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='utility.city'),
        ),
        migrations.AlterField(
            model_name='approx',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utility.city'),
        ),
        migrations.RemoveField(
            model_name='locality',
            name='parent',
        ),
        migrations.AlterField(
            model_name='company',
            name='locality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='utility.locality'),
        ),
        migrations.AlterField(
            model_name='approx',
            name='locality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utility.locality'),
        ),
    ]

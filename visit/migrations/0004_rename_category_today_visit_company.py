# Generated by Django 5.0.1 on 2024-11-10 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visit', '0003_remove_today_visit_title_today_visit_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='today_visit',
            old_name='category',
            new_name='company',
        ),
    ]

# Generated by Django 5.0.1 on 2024-12-11 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0006_company_about'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='title',
        ),
        migrations.AddField(
            model_name='company',
            name='company_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]

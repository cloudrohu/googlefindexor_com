# Generated by Django 4.2 on 2024-06-09 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0004_alter_company_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]

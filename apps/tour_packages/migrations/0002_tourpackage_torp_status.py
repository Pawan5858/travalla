# Generated by Django 5.0.4 on 2025-05-08 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour_packages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourpackage',
            name='torp_status',
            field=models.TextField(blank=True, default='AC', null=True),
        ),
    ]

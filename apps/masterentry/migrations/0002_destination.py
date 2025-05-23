# Generated by Django 5.0.4 on 2025-05-08 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterentry', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('dest_id', models.AutoField(primary_key=True, serialize=False)),
                ('dest_name', models.CharField(max_length=100)),
                ('dest_country', models.CharField(blank=True, max_length=50, null=True)),
                ('dest_state', models.CharField(blank=True, max_length=50, null=True)),
                ('dest_description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Destinations',
            },
        ),
    ]

# Generated by Django 5.1.5 on 2025-03-06 04:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0007_alter_padd_db_services'),
    ]

    operations = [
        migrations.AlterField(
            model_name='padd_db',
            name='Services',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='service.service_db'),
        ),
    ]

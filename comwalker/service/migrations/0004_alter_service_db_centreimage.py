# Generated by Django 5.0.7 on 2025-01-17 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_padd_db'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service_db',
            name='CentreImage',
            field=models.ImageField(upload_to='servicereg'),
        ),
    ]

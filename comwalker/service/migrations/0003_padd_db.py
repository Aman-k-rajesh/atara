# Generated by Django 4.2.17 on 2024-12-27 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_rename_com_db_service_db'),
    ]

    operations = [
        migrations.CreateModel(
            name='padd_DB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Productimage', models.ImageField(upload_to='service')),
                ('Name', models.CharField(max_length=250)),
                ('Colour', models.CharField(max_length=350)),
                ('Memorycapacity', models.CharField(max_length=250)),
                ('Description', models.CharField(max_length=750)),
                ('Price', models.CharField(max_length=250)),
                ('Details', models.CharField(max_length=1000)),
                ('Review', models.CharField(max_length=750)),
                ('Services', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='service.service_db')),
            ],
        ),
    ]

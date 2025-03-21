# Generated by Django 4.2.16 on 2024-12-17 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='com_TB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FullName', models.CharField(max_length=250)),
                ('Email', models.EmailField(max_length=450)),
                ('Location', models.CharField(max_length=350)),
                ('Address', models.CharField(max_length=350)),
                ('PinAddress', models.CharField(max_length=350)),
                ('Image', models.ImageField(upload_to='user')),
                ('Password', models.CharField(max_length=50)),
            ],
        ),
    ]

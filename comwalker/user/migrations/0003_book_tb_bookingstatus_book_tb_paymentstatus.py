# Generated by Django 4.2.17 on 2025-01-04 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_book_tb'),
    ]

    operations = [
        migrations.AddField(
            model_name='book_tb',
            name='Bookingstatus',
            field=models.BooleanField(default='False'),
        ),
        migrations.AddField(
            model_name='book_tb',
            name='Paymentstatus',
            field=models.BooleanField(default='False'),
        ),
    ]

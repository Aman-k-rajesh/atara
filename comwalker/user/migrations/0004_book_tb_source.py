# Generated by Django 5.0.7 on 2025-01-15 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_book_tb_bookingstatus_book_tb_paymentstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='book_tb',
            name='source',
            field=models.CharField(choices=[('database', 'Database'), ('dataset', 'Dataset')], default='database', max_length=50),
        ),
    ]

# Generated by Django 4.2.17 on 2025-01-10 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='prjctadm_DB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=250)),
                ('Email', models.EmailField(max_length=450)),
                ('Password', models.CharField(max_length=50)),
            ],
        ),
    ]

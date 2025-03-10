# Generated by Django 5.1.5 on 2025-03-06 10:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0009_alter_padd_db_services'),
        ('user', '0008_alter_com_tb_address_alter_com_tb_email_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(blank=True, max_length=150, null=True)),
                ('pname', models.CharField(blank=True, max_length=150, null=True)),
                ('rating', models.IntegerField()),
                ('comment', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='review_images/')),
                ('video', models.FileField(blank=True, null=True, upload_to='review_videos/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='service.padd_db')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

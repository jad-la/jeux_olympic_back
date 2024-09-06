# Generated by Django 5.1.1 on 2024-09-06 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(max_length=190),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='qr_code',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='security_key',
            field=models.CharField(max_length=200),
        ),
    ]

# Generated by Django 5.1.1 on 2024-09-06 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_alter_event_location_alter_ticket_qr_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='offer',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='qr_code',
            field=models.CharField(max_length=210, unique=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='security_key',
            field=models.CharField(max_length=210),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=190),
        ),
        migrations.AlterField(
            model_name='user',
            name='security_key',
            field=models.CharField(max_length=200),
        ),
    ]

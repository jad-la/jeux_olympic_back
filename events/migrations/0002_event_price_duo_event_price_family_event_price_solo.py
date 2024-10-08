# Generated by Django 5.1.1 on 2024-09-11 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='price_duo',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='price_family',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='price_solo',
            field=models.DecimalField(decimal_places=2, default=30, max_digits=6),
            preserve_default=False,
        ),
    ]

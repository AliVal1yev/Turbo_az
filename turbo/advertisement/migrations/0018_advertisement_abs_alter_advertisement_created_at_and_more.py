# Generated by Django 5.0.6 on 2024-05-29 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0017_advertisement_hatch_advertisement_parking_radar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='abs',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='parking_radar',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='updated_at',
            field=models.DateTimeField(),
        ),
    ]

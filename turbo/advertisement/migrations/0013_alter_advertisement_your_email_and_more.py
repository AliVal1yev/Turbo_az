# Generated by Django 5.0.6 on 2024-05-24 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0012_advertisement_phone_number_advertisement_your_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='your_email',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='your_name',
            field=models.CharField(max_length=32),
        ),
    ]
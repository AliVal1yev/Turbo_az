# Generated by Django 5.0.6 on 2024-05-24 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0014_alter_advertisement_your_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='your_email',
            field=models.EmailField(max_length=32),
        ),
    ]

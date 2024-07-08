# Generated by Django 5.0.6 on 2024-07-08 10:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='FuelType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='CarAdvertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(null=True)),
                ('color', models.CharField(max_length=16)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('engine', models.FloatField(null=True)),
                ('mileage', models.FloatField(null=True)),
                ('description', models.TextField(max_length=3000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('your_name', models.CharField(max_length=32)),
                ('phone_number', models.IntegerField(null=True)),
                ('your_email', models.EmailField(max_length=32)),
                ('car_status', models.CharField(blank=True, choices=[('APPROVE', 'approve'), ('PENDING', 'pending'), ('REJECTED', 'rejected')], default='PENDING', max_length=32, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisement.carmodel')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisement.carname')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisement.category')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisement.city')),
                ('equipment', models.ManyToManyField(to='advertisement.equipment')),
                ('fuel_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisement.fueltype')),
            ],
        ),
        migrations.CreateModel(
            name='CarImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='media/%Y/%m/%d')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='advertisement.caradvertisement')),
            ],
        ),
        migrations.AddField(
            model_name='carmodel',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisement.carname'),
        ),
    ]

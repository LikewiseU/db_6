# Generated by Django 5.0 on 2023-12-13 23:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unicomapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyCafe',
            fields=[
                ('cafe_id', models.AutoField(primary_key=True, serialize=False)),
                ('cafe_name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('link', models.URLField()),
            ],
            options={
                'db_table': 'study_cafe',
            },
        ),
        migrations.CreateModel(
            name='StudyCafeRoom',
            fields=[
                ('study_cafe_room_id', models.AutoField(primary_key=True, serialize=False)),
                ('room_id', models.IntegerField()),
                ('room_name', models.CharField(max_length=100)),
                ('hourly_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('room_capacity', models.IntegerField()),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='unicomapp.studycafe')),
            ],
            options={
                'db_table': 'study_cafe_room',
            },
        ),
        migrations.CreateModel(
            name='StudyCafeRoomReservation',
            fields=[
                ('reservation_id', models.AutoField(primary_key=True, serialize=False)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('billing_date', models.DateField()),
                ('study', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unicomapp.study')),
                ('study_cafe_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unicomapp.studycaferoom')),
            ],
            options={
                'db_table': 'study_cafe_room_reservation',
            },
        ),
    ]

# Generated by Django 3.1.4 on 2021-09-10 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flights',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField(verbose_name='Flight Date')),
                ('Heurelocale', models.TimeField(verbose_name='Depart hour')),
                ('Aéroport_départ', models.CharField(max_length=200, verbose_name='Depart Airport')),
                ('depart_x', models.CharField(max_length=200, verbose_name='Depart X ')),
                ('depart_y', models.CharField(max_length=200, verbose_name='Depart Y ')),
                ('départ_IATA', models.CharField(max_length=3, verbose_name='Depart Airport IATA')),
                ('Aéroport_Destination', models.CharField(max_length=200, verbose_name='Arrival Airport ')),
                ('destination_x', models.CharField(max_length=200, verbose_name='Destination X ')),
                ('destination_y', models.CharField(max_length=200, verbose_name='Destination Y')),
                ('destination_IATA', models.CharField(max_length=3, verbose_name='Arrival Airport IATA')),
                ('HeureArrivé', models.TimeField(verbose_name='Arrival hour')),
                ('Durée_IATA', models.TimeField(verbose_name='Flight duration')),
                ('Compagnie', models.CharField(max_length=120, verbose_name='Flight Compagnie')),
                ('Num_Vol', models.CharField(max_length=200, verbose_name='flight number ')),
                ('Prix_Camp1', models.CharField(max_length=200, verbose_name='Flight Price')),
            ],
        ),
        migrations.DeleteModel(
            name='Flight',
        ),
    ]

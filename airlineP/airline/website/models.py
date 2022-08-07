from django.db import models
from django.utils.translation import gettext as _


class Flights (models.Model):
    Date = models.DateField('Flight Date')
    Heurelocale = models.TimeField('Depart hour')
    Aéroport_départ = models.CharField('Depart Airport', max_length=200)
    depart_x = models.CharField('Depart X ', max_length=200)
    depart_y = models.CharField('Depart Y ', max_length=200)
    départ_IATA = models.CharField('Depart Airport IATA', max_length=200)
    Aéroport_Destination = models.CharField('Arrival Airport ', max_length=200)
    destination_x = models.CharField('Destination X ', max_length=200)
    destination_y = models.CharField('Destination Y', max_length=200)
    destination_IATA = models.CharField('Arrival Airport IATA', max_length=200)
    HeureArrivé = models.TimeField('Arrival hour')
    Durée_trajet = models.TimeField('Flight duration')
    Compagnie = models.CharField('Flight Compagnie', max_length=200)
    Num_Vol = models.CharField('flight number ', max_length=300)
    Prix_Camp1 = models.CharField('Flight Price', max_length=200)

    def __str__(self):
        return 'Flight Number : ' + self.Num_Vol


class Flightt (models.Model):
    Date = models.DateField('Flight Date')
    Heurelocale = models.TimeField('Depart hour')
    Aéroport_départ = models.CharField('Depart Airport', max_length=200)
    depart_x = models.CharField('Depart X ', max_length=200)
    depart_y = models.CharField('Depart Y ', max_length=200)
    départ_IATA = models.CharField('Depart Airport IATA', max_length=200)
    Aéroport_Destination = models.CharField('Arrival Airport ', max_length=200)
    destination_x = models.CharField('Destination X ', max_length=200)
    destination_y = models.CharField('Destination Y', max_length=200)
    destination_IATA = models.CharField('Arrival Airport IATA', max_length=200)
    HeureArrivé = models.TimeField('Arrival hour')
    Durée_trajet = models.TimeField('Flight duration')
    Compagnie = models.CharField('Flight Compagnie', max_length=120)
    Num_Vol = models.CharField('flight number ', max_length=200)
    Prix_Camp1 = models.CharField('Flight Price', max_length=200)

    def __str__(self):
        return 'Flight Number :' + self.Num_Vol

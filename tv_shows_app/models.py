from __future__ import unicode_literals
from django.db import models
import datetime

class Network(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TvShowManager(models.Manager):
    def validador_basico(self, postData):
        errors = {}

        if len(postData['title']) < 2:
            errors['title'] = "title must be at least 2 characters long";

        #si el usuario no seleccionó ningun network y dejo la opción que pusimos por defecto en el <select> en html
        if postData['network'] == "Open this select menu":
            errors['release_date'] = "network is necesary";

        if postData['network'] != "Open this select menu":
            network = Network.objects.get(id=postData['network'])
            if len(network.name) < 3:
                errors['network'] = "network must be at least 3 characters long";

        if postData['release_date'] == "":
            errors['release_date'] = "release date is necesary";

        #=====================================================================================
        if postData['release_date'] != "":
            #Comprobamos que la fecha de lanzamiento sea la fecha de hoy o una anterior
            #no puede ser una fehca futura
            hoy = datetime.date.today()
            release =datetime.datetime.strptime(postData['release_date'], "%Y-%m-%d").date()

            if(release > hoy): #conultamos si la fecha ingresada por el usuario es mayor a la fecha actual
                errors['release_date'] = "The release date cannot be in the future tense"
        #=====================================================================================
        if len(postData['description']) > 0:
            if len(postData['description']) < 10:
                errors['description'] = "description must be at least 3 characters long"; 

        return errors


class TvShow(models.Model):
    title = models.CharField(max_length=45)
    network = models.ForeignKey(Network,
                            null=False, #puede ser nulo
                            related_name='tvshows',
                            on_delete=models.CASCADE)
    release_date = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TvShowManager()


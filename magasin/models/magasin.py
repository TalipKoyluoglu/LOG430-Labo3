from django.db import models


class Magasin(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)

    def __str__(self):
        return self.nom

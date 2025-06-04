from django.db import models

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    categorie = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    quantite_stock = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom
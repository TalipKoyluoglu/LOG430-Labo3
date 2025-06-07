from django.db import models  # type: ignore
from .produit import Produit
from .magasin import Magasin


class StockCentral(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()

    def __str__(self):
        return f"{self.produit.nom} - Central: {self.quantite}"


class StockLocal(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    magasin = models.ForeignKey(Magasin, on_delete=models.CASCADE)
    quantite = models.IntegerField()

    def __str__(self):
        return f"{self.produit.nom} - {self.magasin.nom}: {self.quantite}"


class DemandeReapprovisionnement(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    magasin = models.ForeignKey(Magasin, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, default="en_attente")  # à traiter dans UC6

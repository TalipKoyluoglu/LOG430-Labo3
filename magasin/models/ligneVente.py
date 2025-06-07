from django.db import models
from .vente import Vente
from .produit import Produit


class LigneVente(models.Model):
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE, related_name="lignes")
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom}"

from django.db import models
from .magasin import Magasin

class Vente(models.Model):
    magasin = models.ForeignKey(Magasin, on_delete=models.CASCADE, related_name="ventes")
    date_vente = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Vente {self.id} - {self.date_vente.date()}"
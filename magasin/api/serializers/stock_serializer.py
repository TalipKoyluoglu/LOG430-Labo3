from rest_framework import serializers
from magasin.models.stock import StockLocal


class StockLocalSerializer(serializers.ModelSerializer):
    produit_nom = serializers.CharField(source="produit.nom", read_only=True)
    magasin_nom = serializers.CharField(source="magasin.nom", read_only=True)

    class Meta:
        model = StockLocal
        fields = ["id", "produit", "magasin", "quantite", "produit_nom", "magasin_nom"]

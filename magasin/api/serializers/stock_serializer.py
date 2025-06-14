from rest_framework import serializers
from magasin.models.stock import StockLocal

class StockLocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockLocal
        fields = ['id', 'produit', 'magasin', 'quantite']
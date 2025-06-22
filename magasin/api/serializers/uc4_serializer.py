from rest_framework import serializers


class ProduitUpdateSerializer(serializers.Serializer):
    nom = serializers.CharField(max_length=100, required=False)
    categorie = serializers.CharField(max_length=100, required=False)
    prix = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    description = serializers.CharField(allow_blank=True, required=False)

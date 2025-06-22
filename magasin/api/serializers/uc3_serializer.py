from rest_framework import serializers


class PerformanceMagasinSerializer(serializers.Serializer):
    magasin = serializers.CharField()
    chiffre_affaires = serializers.DecimalField(max_digits=10, decimal_places=2)
    ruptures = serializers.IntegerField()
    surstock = serializers.IntegerField()
    tendances = serializers.CharField()

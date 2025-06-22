import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
class TestPerformanceMagasinsAPI:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("api_v1_dashboard")

        # Création des données de test
        from magasin.models.magasin import Magasin
        from magasin.models.produit import Produit
        from magasin.models.vente import Vente
        from magasin.models.ligneVente import LigneVente
        from magasin.models.stock import StockLocal

        self.magasin = Magasin.objects.create(
            nom="Magasin Test", adresse="123 rue Test"
        )

        self.produit = Produit.objects.create(
            nom="Produit Test",
            categorie="Test",
            prix=10.00,
            quantite_stock=100,
            description="Description test",
        )

        # Création d'une vente
        self.vente = Vente.objects.create(magasin=self.magasin, total=50.00)

        LigneVente.objects.create(
            vente=self.vente, produit=self.produit, quantite=5, prix_unitaire=10.00
        )

        # Création d'un stock
        StockLocal.objects.create(
            magasin=self.magasin, produit=self.produit, quantite=50
        )

    def test_get_performance_magasins(self):
        """Test de l'endpoint GET /api/v1/dashboard/"""
        response = self.client.get(self.url)

        # Affichage de la structure réelle de la réponse
        print("Réponse API UC3:", response.json())

        # Vérification du code de statut
        assert response.status_code == status.HTTP_200_OK

        # Vérification de la structure de la réponse
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        # Vérification des données du magasin de test
        magasin_data = next((m for m in data if m["magasin"] == "Magasin Test"), None)
        assert magasin_data is not None

        # Vérification des indicateurs de performance
        assert "chiffre_affaires" in magasin_data
        assert "ruptures" in magasin_data
        assert "surstock" in magasin_data
        assert "tendances" in magasin_data

        # Vérification des tendances
        assert magasin_data["tendances"] == "Produit Test (5)"

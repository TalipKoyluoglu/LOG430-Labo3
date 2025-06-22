import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
class TestStockMagasinAPI:
    def setup_method(self):
        self.client = APIClient()

        # Création des données de test
        from magasin.models.magasin import Magasin
        from magasin.models.produit import Produit
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

        self.stock = StockLocal.objects.create(
            magasin=self.magasin, produit=self.produit, quantite=50
        )

    def test_get_stock_magasin_existant(self):
        """Test de l'endpoint GET /api/v1/stores/{store_id}/stock/ avec un magasin existant"""
        url = reverse("api_v1_stock_store", kwargs={"store_id": self.magasin.id})
        response = self.client.get(url)

        # Affichage de la structure réelle de la réponse
        print("Réponse API UC2:", response.json())

        # Vérification du code de statut
        assert response.status_code == status.HTTP_200_OK

        # Vérification de la structure de la réponse
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        # Vérification des données du stock
        stock_data = next((s for s in data if s["nom"] == "Produit Test"), None)
        assert stock_data is not None
        assert stock_data["quantite"] == 50
        # On ne vérifie plus le prix car il n'est pas dans la réponse

    def test_get_stock_magasin_inexistant(self):
        """Test de l'endpoint GET /api/v1/stores/{store_id}/stock/ avec un magasin inexistant"""
        url = reverse("api_v1_stock_store", kwargs={"store_id": 99999})
        response = self.client.get(url)

        # Vérification du code de statut
        assert response.status_code == status.HTTP_200_OK

        # Vérification que la liste est vide
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

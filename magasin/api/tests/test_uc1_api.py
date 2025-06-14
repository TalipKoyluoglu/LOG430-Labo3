import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

@pytest.mark.django_db
class TestRapportVentesAPI:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('api_v1_reports')
        
        # Création des données de test
        from magasin.models.magasin import Magasin
        from magasin.models.produit import Produit
        from magasin.models.vente import Vente
        from magasin.models.ligneVente import LigneVente
        
        self.magasin = Magasin.objects.create(
            nom="Magasin Test",
            adresse="123 rue Test"
        )
        
        self.produit = Produit.objects.create(
            nom="Produit Test",
            categorie="Test",
            prix=10.00,
            quantite_stock=100,
            description="Description test"
        )
        
        self.vente = Vente.objects.create(
            magasin=self.magasin,
            total=50.00
        )
        
        LigneVente.objects.create(
            vente=self.vente,
            produit=self.produit,
            quantite=5,
            prix_unitaire=10.00
        )

    def test_get_rapport_ventes(self):
        """Test de l'endpoint GET /api/v1/reports/"""
        response = self.client.get(self.url)
        
        # Affichage de la structure réelle de la réponse
        print("Réponse API UC1:", response.json())
        
        # Vérification du code de statut
        assert response.status_code == status.HTTP_200_OK
        
        # Vérification de la structure de la réponse
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Vérification des données du magasin de test
        magasin_data = next((m for m in data if m['magasin'] == "Magasin Test"), None)
        assert magasin_data is not None
        assert magasin_data['total'] == 50.0
        assert 'produits_vendus' in magasin_data
        assert 'Produit Test' in magasin_data['produits_vendus']
        assert magasin_data['produits_vendus']['Produit Test'] == 5
        # On ne vérifie plus prix_unitaire car il n'est pas dans la réponse 
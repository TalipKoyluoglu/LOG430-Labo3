import pytest
from django.test import Client  # type: ignore

@pytest.mark.django_db
class TestEndToEnd:

    def setup_method(self):
        from magasin.models.magasin import Magasin
        from magasin.models.produit import Produit
        from magasin.models.stock import StockCentral

        self.client = Client()
        self.magasin = Magasin.objects.create(
            nom="Magasin Principal", adresse="Centre-ville"
        )
        self.produit = Produit.objects.create(
            nom="Écran", categorie="Info", prix=120.00, quantite_stock=10
        )
        StockCentral.objects.create(produit=self.produit, quantite=500)

    def test_scenario_demande_et_validation_reappro(self):
        from magasin.models.stock import DemandeReapprovisionnement

        # 1. Créer une demande
        response = self.client.post(
            "/uc2/reapprovisionner/",
            {
                "produit_id": self.produit.id,
                "magasin_id": self.magasin.id,
                "quantite": 15,
            },
        )
        assert response.status_code == 302

        # 2. Vérifier existence
        demande = DemandeReapprovisionnement.objects.get(
            produit=self.produit, magasin=self.magasin
        )
        assert demande.statut == "en_attente"

        # 3. Valider la demande
        response = self.client.post(f"/uc6/valider/{demande.id}/")
        assert response.status_code == 302
        demande.refresh_from_db()
        assert demande.statut in ["approuvée", "refusée"]

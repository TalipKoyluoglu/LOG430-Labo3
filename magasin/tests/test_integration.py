import pytest
from django.test import Client  # type: ignore
from django.urls import reverse  # type: ignore


@pytest.mark.django_db
class TestIntegration:

    def setup_method(self):
        from magasin.models.magasin import Magasin
        from magasin.models.produit import Produit
        from magasin.models.stock import StockCentral

        self.client = Client()
        self.magasin = Magasin.objects.create(nom="Test Magasin", adresse="123 rue A")
        self.produit = Produit.objects.create(
            nom="Test Produit",
            categorie="Informatique",
            prix=10.00,
            quantite_stock=100,
            description="Test Desc",
        )
        StockCentral.objects.create(produit=self.produit, quantite=200)

    def test_uc1_rapport_ventes(self):
        from magasin.models.vente import Vente
        from magasin.models.ligneVente import LigneVente

        vente = Vente.objects.create(magasin=self.magasin, total=100.00)
        LigneVente.objects.create(
            vente=vente, produit=self.produit, quantite=5, prix_unitaire=10.00
        )
        response = self.client.get(reverse("uc1_rapport"))
        assert response.status_code == 200
        assert "Test Produit" in response.content.decode()

    def test_uc2_creation_demande_reappro(self):
        from magasin.models.stock import DemandeReapprovisionnement

        data = {
            "produit_id": self.produit.id,
            "magasin_id": self.magasin.id,
            "quantite": 20,
        }
        response = self.client.post(reverse("uc2_reapprovisionner"), data)
        assert response.status_code == 302
        assert DemandeReapprovisionnement.objects.filter(
            produit=self.produit, magasin=self.magasin
        ).exists()

    def test_uc3_tableau_de_bord(self):
        from magasin.models.vente import Vente
        from magasin.models.ligneVente import LigneVente

        vente = Vente.objects.create(magasin=self.magasin, total=50.00)
        LigneVente.objects.create(
            vente=vente, produit=self.produit, quantite=3, prix_unitaire=10.00
        )
        response = self.client.get("/uc3/dashboard/")
        assert response.status_code == 200
        assert "Test Magasin" in response.content.decode()

    def test_uc4_modification_produit(self):
        response = self.client.post(
            f"/uc4/modifier/{self.produit.id}/",
            {
                "nom": "Produit Modifié",
                "categorie": "Accessoires",
                "prix": 15.00,
                "quantite_stock": 80,
                "description": "Nouveau",
            },
        )
        assert response.status_code == 302
        self.produit.refresh_from_db()
        assert self.produit.nom == "Produit Modifié"

    def test_uc6_validation_demande(self):
        from magasin.models.stock import DemandeReapprovisionnement

        demande = DemandeReapprovisionnement.objects.create(
            produit=self.produit, magasin=self.magasin, quantite=10, statut="en_attente"
        )
        response = self.client.post(reverse("uc6_valider", args=[demande.id]))
        assert response.status_code == 302
        demande.refresh_from_db()
        assert demande.statut in ["approuvée", "refusée"]

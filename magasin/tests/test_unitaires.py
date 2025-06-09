import pytest
from magasin.controllers.uc2_stock import UC2_StockControleur
from magasin.controllers.uc6_validation import UC6_ValidationControleur


@pytest.mark.django_db
class TestUnitUC2:

    def setup_method(self):
        from magasin.models.magasin import Magasin
        from magasin.models.produit import Produit
        from magasin.models.stock import StockCentral

        self.controleur = UC2_StockControleur()
        self.magasin = Magasin.objects.create(nom="Unit Magasin", adresse="Rue A")
        self.produit = Produit.objects.create(
            nom="Clavier", categorie="Info", prix=20.0, quantite_stock=50
        )
        StockCentral.objects.create(produit=self.produit, quantite=100)

    def test_creer_demande_reapprovisionnement(self):
        from magasin.models.stock import DemandeReapprovisionnement

        success = self.controleur.creer_demande_reapprovisionnement(
            produit_id=self.produit.id, magasin_id=self.magasin.id, quantite=10
        )
        assert success is True
        assert DemandeReapprovisionnement.objects.filter(
            produit=self.produit, magasin=self.magasin
        ).exists()


@pytest.mark.django_db
class TestUnitUC6:

    def setup_method(self):
        from magasin.models.magasin import Magasin
        from magasin.models.produit import Produit
        from magasin.models.stock import StockCentral, DemandeReapprovisionnement

        self.controleur = UC6_ValidationControleur()
        self.magasin = Magasin.objects.create(nom="Test", adresse="XYZ")
        self.produit = Produit.objects.create(
            nom="Souris", categorie="Info", prix=15.0, quantite_stock=40
        )
        StockCentral.objects.create(produit=self.produit, quantite=50)
        self.demande = DemandeReapprovisionnement.objects.create(
            produit=self.produit, magasin=self.magasin, quantite=20, statut="en_attente"
        )

    def test_valider_demande_success(self):
        result = self.controleur.valider_demande(self.demande.id)
        self.demande.refresh_from_db()
        assert result is True
        assert self.demande.statut == "approuvée"

    def test_valider_demande_insuffisant(self):
        self.demande.quantite = 999
        self.demande.save()
        result = self.controleur.valider_demande(self.demande.id)
        self.demande.refresh_from_db()
        assert result is False
        assert self.demande.statut == "refusée"

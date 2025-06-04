from magasin.models.stock import StockCentral
from magasin.models.produit import Produit
from magasin.models.magasin import Magasin
from magasin.models.stock import DemandeReapprovisionnement

class UC2_StockControleur:

    def obtenir_stock_central(self):
        return StockCentral.objects.select_related("produit").all()

    def creer_demande_reapprovisionnement(self, produit_id, magasin_id, quantite):
        try:
            DemandeReapprovisionnement.objects.create(
                produit_id=produit_id,
                magasin_id=magasin_id,
                quantite=quantite
            )
            return True
        except Exception as e:
            print(f"[ERREUR] Création de la demande échouée : {e}")
            return False

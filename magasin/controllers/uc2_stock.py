from magasin.services.uc2_service import (
    obtenir_stock_central,
    creer_demande_reapprovisionnement,
)


class UC2_StockControleur:
    def obtenir_stock_central(self):
        return obtenir_stock_central()

    def creer_demande_reapprovisionnement(self, produit_id, magasin_id, quantite):
        return creer_demande_reapprovisionnement(produit_id, magasin_id, quantite)

class UC2_StockControleur:

    def obtenir_stock_central(self):
        from magasin.models.stock import StockCentral

        return StockCentral.objects.select_related("produit").all()

    def creer_demande_reapprovisionnement(self, produit_id, magasin_id, quantite):
        from magasin.models.stock import DemandeReapprovisionnement

        try:
            DemandeReapprovisionnement.objects.create(
                produit_id=produit_id, magasin_id=magasin_id, quantite=quantite
            )
            return True
        except Exception as e:
            print(f"[ERREUR] Création de la demande échouée : {e}")
            return False

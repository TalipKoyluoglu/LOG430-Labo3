from magasin.services.uc4_service import get_produit, modifier_produit


class UC4_ProduitControleur:

    def get_produit(self, produit_id):
        return get_produit(produit_id)

    def modifier_produit(
        self, produit_id, nouveau_nom, nouveau_prix, nouvelle_description
    ):
        return modifier_produit(
            produit_id, nouveau_nom, nouveau_prix, nouvelle_description
        )

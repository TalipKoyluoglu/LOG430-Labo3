from magasin.models.produit import Produit


class UC4_ProduitControleur:

    def get_produit(self, produit_id):
        try:
            return Produit.objects.get(id=produit_id)
        except Produit.DoesNotExist:
            return None

    def modifier_produit(
        self, produit_id, nouveau_nom, nouveau_prix, nouvelle_description
    ):
        try:
            produit = Produit.objects.get(id=produit_id)
            produit.nom = nouveau_nom
            produit.prix = nouveau_prix
            produit.description = nouvelle_description
            produit.save()
            return True
        except Exception as e:
            print(f"[ERREUR] Modification du produit échouée : {e}")
            return False

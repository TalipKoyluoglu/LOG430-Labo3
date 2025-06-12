from magasin.models.produit import Produit

def get_produit(produit_id):
    try:
        return Produit.objects.get(id=produit_id)
    except Produit.DoesNotExist:
        return None

def modifier_produit(produit_id, nouveau_nom, nouveau_prix, nouvelle_description):
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

def modifier_produitAPI(produit_id, data):
    try:
        produit = Produit.objects.get(id=produit_id)
        produit.nom = data.get("nom", produit.nom)
        produit.prix = data.get("prix", produit.prix)
        produit.description = data.get("description", produit.description)
        produit.categorie = data.get("categorie", produit.categorie)
        produit.save()
        return produit
    except Produit.DoesNotExist:
        return None
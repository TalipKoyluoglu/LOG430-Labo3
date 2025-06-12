from magasin.models.stock import StockCentral, DemandeReapprovisionnement
from magasin.models.stock import StockLocal
from magasin.models.produit import Produit

def obtenir_stock_central():
    return StockCentral.objects.select_related("produit").all()

def creer_demande_reapprovisionnement(produit_id, magasin_id, quantite):
    try:
        DemandeReapprovisionnement.objects.create(
            produit_id=produit_id, magasin_id=magasin_id, quantite=quantite
        )
        return True
    except Exception as e:
        print(f"[ERREUR] Création de la demande échouée : {e}")
        return False
    
def obtenir_stock_magasin(magasin_id):
    try:
        stock_entries = StockLocal.objects.filter(magasin_id=magasin_id).select_related("produit")
    except StockLocal.DoesNotExist:
        return []

    reponse = []
    for stock in stock_entries:
        reponse.append({
            "produit_id": stock.produit.id,
            "nom": stock.produit.nom,
            "quantite": stock.quantite
        })

    return reponse
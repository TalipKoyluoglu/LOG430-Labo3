from magasin.models.stock import (
    DemandeReapprovisionnement,
    StockCentral,
    StockLocal,
)

def get_demandes_en_attente():
    return DemandeReapprovisionnement.objects.filter(statut="en_attente")

def valider_demande(demande_id):
    try:
        demande = DemandeReapprovisionnement.objects.get(id=demande_id)

        produit = demande.produit
        magasin = demande.magasin
        quantite = demande.quantite

        stock_central = StockCentral.objects.get(produit=produit)

        if quantite <= 0 or stock_central.quantite < quantite:
            demande.statut = "refusée"
            demande.save()
            return False

        stock_local, created = StockLocal.objects.get_or_create(
            produit=produit, magasin=magasin, defaults={"quantite": 0}
        )

        stock_central.quantite -= quantite
        stock_local.quantite += quantite

        stock_central.save()
        stock_local.save()

        demande.statut = "approuvée"
        demande.save()
        return True

    except DemandeReapprovisionnement.DoesNotExist:
        return False
    except Exception as e:
        print(f"[ERREUR] UC6 - Validation échouée : {e}")
        return False

def rejeter_demande(demande_id):
    try:
        demande = DemandeReapprovisionnement.objects.get(id=demande_id)
        demande.statut = "refusée"
        demande.save()
        return True
    except DemandeReapprovisionnement.DoesNotExist:
        return False
    except Exception as e:
        print(f"[ERREUR] UC6 - Rejet échoué : {e}")
        return False

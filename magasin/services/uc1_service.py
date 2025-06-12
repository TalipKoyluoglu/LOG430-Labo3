from magasin.models import Vente, LigneVente, Magasin, StockLocal

def generer_rapport_consolide():
    rapports = []
    magasins = Magasin.objects.all()

    for magasin in magasins:
        ventes = Vente.objects.filter(magasin=magasin)
        total = sum(
            ligne.quantite * ligne.prix_unitaire
            for vente in ventes
            for ligne in vente.lignes.all()
        )

        produits_vendus = {}
        for vente in ventes:
            for ligne in vente.lignes.all():
                nom_produit = ligne.produit.nom
                produits_vendus[nom_produit] = (
                    produits_vendus.get(nom_produit, 0) + ligne.quantite
                )

        stock_local = {
            s.produit.nom: s.quantite
            for s in StockLocal.objects.filter(magasin=magasin)
        }

        rapports.append({
            "magasin": magasin.nom,
            "total": total,
            "produits_vendus": produits_vendus,
            "stock_local": stock_local,
        })

    return rapports
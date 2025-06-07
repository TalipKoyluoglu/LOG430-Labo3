from magasin.models import Vente, LigneVente, Magasin


def generer_rapport_consolide():
    rapports = []
    magasins = Magasin.objects.all()

    for magasin in magasins:
        ventes = Vente.objects.filter(magasin=magasin)
        total_magasin = sum(v.total for v in ventes)
        produits_vendus = {}

        for vente in ventes:
            for ligne in vente.lignes.all():
                produit = ligne.produit.nom
                quantite = ligne.quantite
                produits_vendus[produit] = produits_vendus.get(produit, 0) + quantite

        rapports.append(
            {
                "magasin": magasin.nom,
                "total": total_magasin,
                "produits_vendus": produits_vendus,
            }
        )

    return rapports

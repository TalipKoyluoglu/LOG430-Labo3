from magasin.models import Magasin, Vente, LigneVente, StockLocal, Produit
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.contrib import messages


def rapport_ventes(request):
    rapports = []

    for magasin in Magasin.objects.all():
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

        rapports.append(
            {
                "magasin": magasin.nom,
                "total": total,
                "produits_vendus": produits_vendus,
                "stock_local": stock_local,
            }
        )

    return render(request, "magasin/uc1_rapport.html", {"rapports": rapports})


def afficher_formulaire_vente(request):
    magasins = Magasin.objects.all()
    produits = Produit.objects.all()
    return render(
        request,
        "magasin/effectuerVente.html",
        {"magasins": magasins, "produits": produits},
    )


@require_http_methods(["POST", "GET"])
def enregistrer_vente(request):
    if request.method == "GET":
        messages.error(
            request, "Accès direct interdit. Veuillez utiliser le formulaire."
        )
        return redirect("uc1_effectuer_vente")

    magasin_id = request.POST.get("magasin_id")
    produit_id = request.POST.get("produit_id")
    quantite = int(request.POST.get("quantite"))

    magasin = Magasin.objects.get(pk=magasin_id)
    produit = Produit.objects.get(pk=produit_id)

    stock_local = StockLocal.objects.filter(magasin=magasin, produit=produit).first()

    if not stock_local:
        messages.error(
            request, "Ce produit n'existe pas dans le stock local de ce magasin."
        )
        return redirect("ajouter_vente")

    if stock_local.quantite < quantite:
        messages.error(request, "Stock insuffisant pour ce produit.")
        return redirect("ajouter_vente")

    vente = Vente.objects.create(magasin=magasin, total=0)

    LigneVente.objects.create(
        vente=vente, produit=produit, quantite=quantite, prix_unitaire=produit.prix
    )

    vente.total = quantite * produit.prix
    vente.save()

    stock_local.quantite -= quantite
    stock_local.save()

    messages.success(request, "Vente enregistrée avec succès.")
    return redirect("uc1_rapport")

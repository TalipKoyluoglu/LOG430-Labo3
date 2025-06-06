from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib import messages # type: ignore
from magasin.controllers.uc4_produit import UC4_ProduitControleur
from magasin.models.produit import Produit

controleur = UC4_ProduitControleur()

def uc4_modifier_produit(request, produit_id):
    produit = controleur.get_produit(produit_id)
    if not produit:
        messages.error(request, "❌ Produit introuvable.")
        return redirect("uc3_dashboard")  # ou une autre vue par défaut

    if request.method == "POST":
        nom = request.POST.get("nom")
        prix = request.POST.get("prix")
        description = request.POST.get("description")

        success = controleur.modifier_produit(produit_id, nom, prix, description)

        if success:
            messages.success(request, "✅ Produit modifié avec succès.")
            return redirect("uc4_modifier_produit", produit_id=produit_id)
        else:
            messages.error(request, "❌ Échec lors de la modification du produit.")

    return render(request, "magasin/uc4_modifProduit.html", {"produit": produit})

def uc4_lister_produits(request):
    produits = Produit.objects.all()
    return render(request, "magasin/uc4_liste.html", {"produits": produits})
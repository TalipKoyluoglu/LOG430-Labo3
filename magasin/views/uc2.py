from django.shortcuts import render, redirect
from django.contrib import messages
from magasin.controllers.uc2_stock import UC2_StockControleur
from magasin.models.magasin import Magasin

controleur = UC2_StockControleur()

def uc2_stock(request):
    stocks = controleur.obtenir_stock_central()
    magasins = Magasin.objects.all()
    return render(request, "magasin/uc2_stock.html", {"stocks": stocks, "magasins": magasins})

def uc2_reapprovisionner(request):
    if request.method == "POST":
        produit_id = request.POST.get("produit_id")
        magasin_id = request.POST.get("magasin_id")
        quantite = int(request.POST.get("quantite"))

        success = controleur.creer_demande_reapprovisionnement(produit_id, magasin_id, quantite)
        if success:
            messages.success(request, "✅ Demande de réapprovisionnement créée avec succès.")
        else:
            messages.error(request, "❌ Échec lors de la création de la demande.")
    return redirect("uc2_stock")

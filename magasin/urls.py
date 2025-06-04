from django.urls import path
from magasin.views.uc1 import rapport_ventes
from magasin.views.uc2 import uc2_stock, uc2_reapprovisionner
from magasin.views.uc1 import afficher_formulaire_vente
from magasin.views.uc1 import enregistrer_vente

urlpatterns = [
    path("uc1/rapport/", rapport_ventes, name="uc1_rapport"),
    path("uc2/stock/", uc2_stock, name="uc2_stock"),
    path("uc2/reapprovisionner/", uc2_reapprovisionner, name="uc2_reapprovisionner"),
    path("uc1/ajouter_vente/", afficher_formulaire_vente, name="ajouter_vente"),
    path("uc1/enregistrer/", enregistrer_vente, name="uc1_enregistrer_vente"),
]

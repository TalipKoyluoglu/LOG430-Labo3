from django.urls import path
from django.views.generic.base import RedirectView
from magasin.views.uc1 import rapport_ventes
from magasin.views.uc2 import uc2_stock, uc2_reapprovisionner
from magasin.views.uc1 import afficher_formulaire_vente
from magasin.views.uc1 import enregistrer_vente
from magasin.views.uc3 import uc3_dashboard
from magasin.views.uc4 import uc4_lister_produits, uc4_modifier_produit
from magasin.views.uc6 import uc6_demandes, uc6_rejeter, uc6_valider
from magasin.api import urls as api_urls
from magasin.api import swagger_urls

urlpatterns = [
    # Redirection de la page d'accueil vers Swagger
    path("", RedirectView.as_view(url="/swagger/", permanent=False), name="home"),
    path("uc1/rapport/", rapport_ventes, name="uc1_rapport"),
    path("uc2/stock/", uc2_stock, name="uc2_stock"),
    path("uc2/reapprovisionner/", uc2_reapprovisionner, name="uc2_reapprovisionner"),
    path("uc1/ajouter_vente/", afficher_formulaire_vente, name="ajouter_vente"),
    path("uc1/enregistrer/", enregistrer_vente, name="uc1_enregistrer_vente"),
    path("uc3/dashboard/", uc3_dashboard, name="uc3_dashboard"),
    path(
        "uc4/modifier/<int:produit_id>/",
        uc4_modifier_produit,
        name="uc4_modifier_produit",
    ),
    path("uc4/produits/", uc4_lister_produits, name="uc4_lister_produits"),
    path("uc6/demandes/", uc6_demandes, name="uc6_demandes"),
    path("uc6/valider/<int:demande_id>/", uc6_valider, name="uc6_valider"),
    path("uc6/rejeter/<int:demande_id>/", uc6_rejeter, name="uc6_rejeter"),
]

urlpatterns += api_urls.urlpatterns
urlpatterns += swagger_urls.urlpatterns

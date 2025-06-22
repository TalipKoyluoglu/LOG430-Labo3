from django.urls import path
from magasin.api.controllers.uc1_api import RapportVentesAPI
from magasin.api.controllers.uc2_api import StockMagasinAPI, StockMagasinListAPI
from magasin.api.controllers.uc3_api import PerformanceMagasinsAPI
from magasin.api.controllers.uc4_api import ProduitUpdateAPI

urlpatterns = [
    path("api/v1/reports/", RapportVentesAPI.as_view(), name="api_v1_reports"),
    path(
        "api/v1/stores/<int:store_id>/stock/",
        StockMagasinAPI.as_view(),
        name="api_v1_stock_store",
    ),
    path(
        "api/v1/stores/<int:store_id>/stock/list/",
        StockMagasinListAPI.as_view(),
        name="api_v1_stock_store_list",
    ),
    path(
        "api/v1/dashboard/", PerformanceMagasinsAPI.as_view(), name="api_v1_dashboard"
    ),
    path(
        "api/v1/products/<int:produit_id>/",
        ProduitUpdateAPI.as_view(),
        name="api_v1_produit_update",
    ),
]

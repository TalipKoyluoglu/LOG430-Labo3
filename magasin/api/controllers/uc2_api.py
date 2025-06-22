from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from magasin.services.uc2_service import obtenir_stock_magasin
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import ListAPIView
from magasin.models.stock import StockLocal
from magasin.api.serializers.stock_serializer import StockLocalSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
import django_filters


class StockLocalFilter(django_filters.FilterSet):
    produit__nom = django_filters.CharFilter(
        field_name="produit__nom", lookup_expr="icontains"
    )
    quantite = django_filters.NumberFilter(field_name="quantite")

    class Meta:
        model = StockLocal
        fields = ["produit__nom", "quantite"]


class StockMagasinAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Consulter le stock d'un magasin",
        operation_description="Retourne le stock actuel du magasin identifié par son ID.",
        tags=["UC2 - Stock magasin"],
        manual_parameters=[
            openapi.Parameter(
                "store_id",
                openapi.IN_PATH,
                description="ID du magasin à consulter",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
    )
    def get(self, request, store_id):
        stock = obtenir_stock_magasin(store_id)
        if stock is None:
            return Response(
                {
                    "timestamp": "2025-06-11T12:00:00Z",
                    "status": 404,
                    "error": "Not Found",
                    "message": f"Magasin avec ID {store_id} introuvable.",
                    "path": f"/api/v1/stores/{store_id}/stock/",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(stock, status=status.HTTP_200_OK)


class StockMagasinListAPI(ListAPIView):
    serializer_class = StockLocalSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = StockLocalFilter
    ordering_fields = ["quantite", "produit__nom"]
    ordering = ["produit__nom"]  # Tri par défaut

    @swagger_auto_schema(
        operation_summary="Liste paginée du stock d'un magasin",
        operation_description="Retourne une liste paginée du stock avec possibilité de filtrage et tri.",
        tags=["UC2 - Stock magasin"],
        manual_parameters=[
            openapi.Parameter(
                "store_id",
                openapi.IN_PATH,
                description="ID du magasin à consulter",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Numéro de page",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
            openapi.Parameter(
                "produit__nom",
                openapi.IN_QUERY,
                description="Filtrer par nom de produit",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                "quantite",
                openapi.IN_QUERY,
                description="Filtrer par quantité exacte",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
            openapi.Parameter(
                "ordering",
                openapi.IN_QUERY,
                description="Trier par champ (quantite, produit__nom). Préfixer par '-' pour ordre décroissant",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        store_id = self.kwargs["store_id"]
        return StockLocal.objects.filter(magasin_id=store_id)

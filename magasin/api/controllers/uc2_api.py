from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from magasin.services.uc2_service import obtenir_stock_magasin
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class StockMagasinAPI(APIView):    
    @swagger_auto_schema(
        operation_summary="Consulter le stock d’un magasin",
        operation_description="Retourne le stock actuel du magasin identifié par son ID.",
        tags=["UC2 - Stock magasin"],
        manual_parameters=[
            openapi.Parameter(
                'store_id',
                openapi.IN_PATH,
                description="ID du magasin à consulter",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
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
                    "path": f"/api/v1/stores/{store_id}/stock/"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(stock, status=status.HTTP_200_OK)
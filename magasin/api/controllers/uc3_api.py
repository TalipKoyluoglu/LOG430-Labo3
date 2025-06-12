from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from magasin.services.uc3_service import get_indicateurs_par_magasin
from magasin.api.serializers.uc3_serializer import PerformanceMagasinSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class PerformanceMagasinsAPI(APIView):

    @swagger_auto_schema(
        operation_summary="Visualiser les performances globales des magasins",
        operation_description="Fournit des indicateurs clés : chiffre d’affaires, ruptures, surstocks et tendances produits des 7 derniers jours.",
        tags=["UC3 - Performances magasins"],
        responses={
            200: PerformanceMagasinSerializer(many=True),
            500: openapi.Response(
                description="Erreur interne du serveur",
                examples={
                    "application/json": {
                        "timestamp": "2025-06-11T12:00:00Z",
                        "status": 500,
                        "error": "Internal Server Error",
                        "message": "Une erreur inattendue est survenue.",
                        "path": "/api/v1/stores/performance/"
                    }
                }
            )
        }
    )
    def get(self, request):
        try:
            performances = get_indicateurs_par_magasin()
            serializer = PerformanceMagasinSerializer(performances, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "timestamp": "2025-06-11T12:00:00Z",
                "status": 500,
                "error": "Internal Server Error",
                "message": str(e),
                "path": "/api/v1/stores/performance/"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

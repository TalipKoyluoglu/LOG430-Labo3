from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from magasin.services.uc1_service import generer_rapport_consolide
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RapportVentesAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Rapport consolidé des ventes",
        operation_description="Retourne un rapport complet pour chaque magasin : total des ventes, produits vendus, stock local.",
        tags=["UC1 - Rapport des ventes"],
    )
    def get(self, request):
        rapport = generer_rapport_consolide()
        return Response(rapport, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from magasin.services.uc4_service import modifier_produitAPI
from magasin.api.serializers.uc4_serializer import ProduitUpdateSerializer
from magasin.api.serializers.uc1_serializer import ProduitSerializer  # Pour la réponse complète
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ProduitUpdateAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Mettre à jour un produit",
        operation_description="Modifie un ou plusieurs attributs d’un produit existant dans la base de données.",
        tags=["UC4 - Mise à jour produit"],
        request_body=ProduitUpdateSerializer,
        responses={
            200: ProduitUpdateSerializer,
            404: openapi.Response(description="Produit non trouvé"),
        }
    )
    def put(self, request, produit_id):
        serializer = ProduitUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        produit = modifier_produitAPI(produit_id, serializer.validated_data)
        if produit is None:
            return Response(
                {
                    "timestamp": "2025-06-11T12:00:00Z",
                    "status": 404,
                    "error": "Not Found",
                    "message": f"Produit avec ID {produit_id} introuvable.",
                    "path": f"/api/v1/products/{produit_id}/"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(ProduitUpdateSerializer(produit.__dict__).data, status=status.HTTP_200_OK)

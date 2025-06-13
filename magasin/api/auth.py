from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

def token_required(view_func):
    def wrapper(self, request, *args, **kwargs):
        token = request.headers.get("Authorization")
        if token != f"Token {settings.API_AUTH_TOKEN}":
            return Response({
                "timestamp": "2025-06-12T00:00:00Z",
                "status": 401,
                "error": "Unauthorized",
                "message": "Token d'accès invalide ou manquant.",
                "path": request.path
            }, status=status.HTTP_401_UNAUTHORIZED)
        return view_func(self, request, *args, **kwargs)
    return wrapper

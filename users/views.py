from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .permissions import IsModerator


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code != 200:
            return response

        token = Token.objects.get(key=response.data['token'])
        user = token.user

        if user.is_banned:
            token.delete()
            return Response(
                {"detail": "Accesso negato: account bannato."},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'is_banned': user.is_banned,
        })

CustomUser = get_user_model()

class BanUserView(APIView):
    permission_classes = [IsAuthenticated, IsModerator]

    def post(self, request, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
            user.is_banned = True
            user.save()
            return Response({"detail": f"Utente {user.username} bannato."})
        except CustomUser.DoesNotExist:
            return Response({"detail": "Utente non trovato."}, status=status.HTTP_404_NOT_FOUND)

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email
        })
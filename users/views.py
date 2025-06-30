import re

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
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

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password1 = request.data.get("password")
        password2 = request.data.get("confirm_password")

        if not username or not email or not password1 or not password2:
            return Response({"error": "Tutti i campi sono obbligatori."}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username già in uso."}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email già registrata, effettua l'accesso."}, status=400)

        try:
            validate_email(email)
        except ValidationError:
            return Response({"error": "Formato email non valido."}, status=400)

        if password1 != password2:
            return Response({"error": "Le password non corrispondono."}, status=400)

        if len(password1) < 8 or not re.search(r"\d", password1):
            return Response({"error": "La password deve essere lunga almeno 8 caratteri e contenere almeno un numero."}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password1)
        return Response({"success": "Registrazione avvenuta con successo."}, status=201)
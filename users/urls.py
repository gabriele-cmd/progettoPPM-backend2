from django.urls import path
from .views import CustomAuthToken, CurrentUserView, BanUserView, RegisterView

urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('me/', CurrentUserView.as_view(), name='user-me'),
    path('ban/<int:user_id>/', BanUserView.as_view(), name='ban-user'),
path('register/', RegisterView.as_view(), name='register'),
]

from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from . import serializer
from django.contrib.auth.models import User
from django.contrib.auth import login, logout

from .tokens import create_jwt_pair_for_user


class RegisterView(generics.CreateAPIView):
    serializer_class = serializer.RegisterSerializer


class LoginView(APIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed("Account does  not exist")
        if user is None:
            raise AuthenticationFailed("User does not exist")
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password")
        tokens = create_jwt_pair_for_user(user)
        login(request, user=user)
        response = {"access_token": tokens['access_token'],
                    "refresh_token": tokens["refresh_token"]}
        return Response(data=response, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            if refresh_token:
                token = RefreshToken(refresh_token)
                logout(request)
                token.blacklist()
            return Response("Logout Successful", status=status.HTTP_200_OK)
        except TokenError:
            raise AuthenticationFailed("Invalid Token")

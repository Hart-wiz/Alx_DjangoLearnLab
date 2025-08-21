from django.shortcuts import render

# Create your views here.
# accounts/views.py
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user, context={'request': request}).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user, context={'request': request}).data,
            'token': token.key
        })

class MeView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user, context={'request': request}).data)

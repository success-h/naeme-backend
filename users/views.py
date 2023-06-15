from django.conf import settings
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import generics, status, parsers
from django.contrib.auth.models import User
from .serializers import *  
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets 
from django.conf import settings
from django_filters import rest_framework as filters
from .authentication import decode_access_token
from rest_framework.exceptions import  AuthenticationFailed
from rest_framework.authentication import get_authorization_header
from .serializers import GoogleSocialAuthSerializer, TwitterAuthSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView




from .serializers import UserSerializer, CustomTokenObtainPairSerializer


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    parser_classes = [parsers.MultiPartParser]

    def perform_create(self, serializer):
        serializer.save(image=self.request.FILES.get('image'))


class SignInView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data

        user = serializer.user
        user_serializer = UserSerializer(user)

        response_data = {
            'tokens': tokens,
            'user': user_serializer.data
        }

        return Response(response_data)
 


class UserView(APIView):
    def get(self, request):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)
            user = User.objects.filter(pk=id).first()
            return Response(UserSerializer(user).data)
        raise AuthenticationFailed('unauthenticated')



class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


class TwitterSocialAuthView(GenericAPIView):
    serializer_class = TwitterAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

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
from .serializers import ForgotPasswordSerializer, ConfirmPasswordResetSerializer, GoogleSocialAuthSerializer, TokenObtainPairSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import PasswordReset
import random
import string




from .serializers import UserSerializer, CustomTokenObtainPairSerializer


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
 


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


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'detail': 'User with this email does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        confirmation_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        print("reset_code:", confirmation_code)
        PasswordReset.objects.create(user=user, confirmation_code=confirmation_code)

        # Send confirmation code via email
        subject = 'Password Reset Confirmation Code'
        message = f'Your confirmation code is: {confirmation_code}'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

        return Response({'detail': 'Confirmation code has been sent to your email.'})




class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)

class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'detail': 'User with this email does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        confirmation_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        PasswordReset.objects.create(user=user, confirmation_code=confirmation_code)

        # Send confirmation code via email
        subject = 'Password Reset Confirmation Code'
        message = f'Your confirmation code is: {confirmation_code}'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

        return Response({'detail': 'Confirmation code has been sent to your email.'})

class ConfirmPasswordResetView(generics.GenericAPIView):
    serializer_class = ConfirmPasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data['confirmation_code']
        new_password = serializer.validated_data['new_password']

        try:
            password_reset = PasswordReset.objects.get(confirmation_code=confirmation_code)
        except PasswordReset.DoesNotExist:
            return Response(
                {'detail': 'Invalid confirmation code.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = password_reset.user
        user.set_password(new_password)
        user.save()
        password_reset.delete()

        return Response({'detail': 'Password has been successfully reset.'})

# class TwitterSocialAuthView(GenericAPIView):
#     serializer_class = TwitterAuthSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.validated_data, status=status.HTTP_200_OK)

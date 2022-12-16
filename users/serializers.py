from rest_framework import serializers, status
from django.utils.text import gettext_lazy as _
from rest_framework.response import Response
from . import google, twitterhelper
from .models import User
import os
from rest_framework.exceptions import AuthenticationFailed
from .register import register_social_user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email", "name", "password", "image"]
        extra_kwargs = {"password": {"write_only": True}}


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        print(user_data)

        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )
        if user_data['aud'] != os.getenv('GOOGLE_EXPO_CLIENT_ID'):
            if user_data['aud'] != os.getenv('GOOGLE_IOS_CLIENT_ID'):
                if user_data['aud'] != os.getenv('GOOGLE_ANDROID_CLIENT_ID'):
                    if user_data['aud'] != os.getenv('GOOGLE_WEB_CLIENT_ID'):
                        raise AuthenticationFailed('authentication source not allowed')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        image = user_data['picture']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name, image=image)


class TwitterAuthSerializer(serializers.Serializer):
    """Handles serialization of twitter related data"""
    access_token_key = serializers.CharField()
    access_token_secret = serializers.CharField()

    def validate(self, attrs):

        access_token_key = attrs.get('access_token_key')
        access_token_secret = attrs.get('access_token_secret')

        user_info = twitterhelper.TwitterAuthTokenVerification.validate_twitter_auth_tokens(
            access_token_key, access_token_secret)
        print("user_info:", user_info)
        try:
            user_id = user_info['id_str']
            email = user_info['email']
            name = user_info['name']
            image = user_info['profile_image_url_https']
            provider = 'twitter'
        except:
            raise serializers.ValidationError(
                'The tokens are invalid or expired. Please login again.'
            )

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name, image=image)

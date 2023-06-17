from django.contrib.auth import authenticate
from .models import User
import os
import random
from rest_framework.exceptions import AuthenticationFailed
import os

def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():
        registered_user = authenticate(
            email=email, password=os.getenv('SOCIAL_SECRET'),
            )
            
        if registered_user is not None:
            user = User.objects.get(email=email)
            user.auth_provider = provider
            user.save()

        return {
            'username': registered_user.name,
            'email': registered_user.email,
            # 'image': registered_user.image,
            'tokens': registered_user.tokens(),
            'auth_provider': registered_user.auth_provider,
            'id': registered_user.id,
            }


    else:
        user = {
            'name': name, 'email': email,
            'password': os.getenv('SOCIAL_SECRET')}
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        new_user = authenticate(
            email=email, password=os.getenv('SOCIAL_SECRET'))
        return {
            'email': new_user.email,
            'username': new_user.name,
            # 'image': new_user.image,
            'tokens': new_user.tokens(),
            'auth_provider': new_user.auth_provider,
            'id': new_user.id,
        }
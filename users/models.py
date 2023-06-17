import uuid
from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required') 
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)


AUTH_PROVIDERS = {'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}

def validate_image(value):
    """
    Validate that the uploaded file is an image.
    """
    if isinstance(value, str):
        return  # Skip validation for string inputs
    elif value:
        width, height = get_image_dimensions(value)
        if width < 10 or height < 10:
            raise ValidationError("The image must have a minimum resolution of 10x10 pixels.")

class User(AbstractBaseUser, PermissionsMixin):
    username = None
    name = models.CharField(max_length=255, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    # image = models.FileField(upload_to='user_images/', validators=[validate_image], null=True, blank=True, default="https://res.cloudinary.com/dp3a4be7p/image/upload/v1686984832/user_eatapc.png")
    image = models.CharField(max_length=3000, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        

class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    print("print:", email_plaintext_message)
    # send_mail(
    #     # title:
    #     "Password Reset for {title}".format(title="Some website title"),
    #     # message:
    #     email_plaintext_message,
    #     # from:
    #     "tech@naeme.app",
    #     # to:
    #     [reset_password_token.user.email]
    # )
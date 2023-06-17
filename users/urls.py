from django.urls import path
from .views import *




urlpatterns = [
    path('account/google/', GoogleSocialAuthView.as_view(), name="google"),
    # path('twitter/', TwitterSocialAuthView.as_view(), name="twitter"),
    path('account/user/', UserView.as_view(), name="user"),
    path('account/signup/', SignUpView.as_view(), name='signup'),
    path('account/signin/', SignInView.as_view(), name='signin'),
    path('account/forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('account/confirm-password-reset/', ConfirmPasswordResetView.as_view(), name='confirm-password-reset'),

    # path('facebook/', FacebookLoginView.as_view(), name="facebook"),
]
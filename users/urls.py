from django.urls import path
from .views import *



urlpatterns = [
    path('google/', GoogleSocialAuthView.as_view(), name="google"),
    path('twitter/', TwitterSocialAuthView.as_view(), name="twitter"),
    path('user/', UserView.as_view(), name="user"),
    # path('facebook/', FacebookLoginView.as_view(), name="facebook"),
]
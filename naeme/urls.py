from xml.dom.minidom import Document
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

 
urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('api/', include('event.urls'), name="events"),
     path('api/account/', include('users.urls')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


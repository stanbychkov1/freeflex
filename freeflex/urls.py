from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import UserRegistrationView


from . import settings
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('register/', UserRegistrationView.as_view(),
         name='register'),
    path('api/', include('api.urls')),
]


urlpatterns += doc_urls


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

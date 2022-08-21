from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.urls import path, include

from ably_auth.views import phone_auth_view

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'phone_auth', phone_auth_view.PhoneAuthViewSet, basename='phone_auth')

urlpatterns = [
    path('', include(router.urls)),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]

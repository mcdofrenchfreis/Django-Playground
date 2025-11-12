"""API URL router for todoapp."""
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .api_views import TodoViewSet
from .auth_views import RegisterAPIView, CustomObtainAuthToken

router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterAPIView.as_view(), name='api-register'),
    path('auth/login/', CustomObtainAuthToken.as_view(), name='api-login'),
]

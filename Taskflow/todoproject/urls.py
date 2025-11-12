"""URL configuration for todoproject project."""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todoapp.urls')),
    path('api/', include('todoapp.api_urls')),
    # Obtain auth token: POST username & password -> {"token": "..."}
    path('api-token-auth/', obtain_auth_token),
]

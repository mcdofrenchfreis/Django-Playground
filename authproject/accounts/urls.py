from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("profile/", views.profile, name="profile"),
    path("login/", views.RememberMeLoginView.as_view(), name="login"),
    # JSON APIs
    path("api/check-username", views.api_check_username, name="api_check_username"),
    path("api/check-email", views.api_check_email, name="api_check_email"),
    path("api/send-email", views.api_send_email, name="api_send_email"),
    path("api/resend-activation", views.api_resend_activation, name="api_resend_activation"),
]

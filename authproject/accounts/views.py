from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.core.mail import send_mail
from django.conf import settings

from .forms import SignUpForm
from .tokens import account_activation_token


class RememberMeLoginView(LoginView):
    def form_valid(self, form):
        remember = self.request.POST.get("remember")
        response = super().form_valid(form)
        if remember:
            # Keep session for 2 weeks
            self.request.session.set_expiry(1209600)
        else:
            # Browser session only
            self.request.session.set_expiry(0)
        return response


def signup(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user: User = form.save(commit=False)
            user.is_active = False
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activation_url = request.build_absolute_uri(
                reverse("accounts:activate", kwargs={"uidb64": uid, "token": token})
            )

            subject = "Activate your account"
            message = render_to_string(
                "accounts/activation_email.txt",
                {"user": user, "activation_url": activation_url},
            )

            user.email_user(subject, message)
            return render(request, "accounts/activation_sent.html")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


def activate(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, "accounts/activation_complete.html")
    else:
        return render(request, "accounts/activation_invalid.html", status=400)


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    return render(request, "accounts/profile.html")


# --- JSON API endpoints ---


@require_GET
def api_check_username(request: HttpRequest) -> JsonResponse:
    username = (request.GET.get("username") or "").strip()
    taken = False
    if username:
        taken = User.objects.filter(username__iexact=username).exists()
    return JsonResponse({"username": username, "available": not taken})


@require_GET
def api_check_email(request: HttpRequest) -> JsonResponse:
    email = (request.GET.get("email") or "").strip()
    taken = False
    if email:
        taken = User.objects.filter(email__iexact=email).exists()
    return JsonResponse({"email": email, "available": not taken})


@csrf_exempt
@require_POST
def api_send_email(request: HttpRequest) -> JsonResponse:
    """Simple email sender API for development.
    Expects JSON: {"to": "email@example.com" or [..], "subject": str, "message": str}
    """
    import json

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    to = payload.get("to")
    subject = payload.get("subject")
    message = payload.get("message")

    if not subject or not message or not to:
        return JsonResponse({"error": "Missing 'to', 'subject', or 'message'."}, status=400)

    if isinstance(to, str):
        recipients = [to]
    elif isinstance(to, list) and all(isinstance(x, str) for x in to):
        recipients = to
    else:
        return JsonResponse({"error": "'to' must be a string or list of strings."}, status=400)

    sent = send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients)
    return JsonResponse({"sent": sent, "recipients": recipients})


@csrf_exempt
@require_POST
def api_resend_activation(request: HttpRequest) -> JsonResponse:
    """Resend activation email for a user by email if not active."""
    import json

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    email = (payload.get("email") or "").strip()
    if not email:
        return JsonResponse({"error": "Missing 'email'."}, status=400)

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        # Don't reveal whether the email exists
        return JsonResponse({"status": "ok"})

    if user.is_active:
        return JsonResponse({"status": "ok", "detail": "already_active"})

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    activation_url = request.build_absolute_uri(
        reverse("accounts:activate", kwargs={"uidb64": uid, "token": token})
    )
    subject = "Activate your account"
    message = render_to_string(
        "accounts/activation_email.txt",
        {"user": user, "activation_url": activation_url},
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    return JsonResponse({"status": "ok"})

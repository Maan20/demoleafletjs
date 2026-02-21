from django.urls import path
from .views import ForgotPasswordView, LoginView, MeView, RegisterView, VerifyOTPView

urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("auth/verify-otp/", VerifyOTPView.as_view()),
    path("auth/login/", LoginView.as_view()),
    path("auth/forgot-password/", ForgotPasswordView.as_view()),
    path("auth/me/", MeView.as_view()),
]

from django.core.mail import send_mail
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import ForgotPasswordSerializer, LoginSerializer, RegisterSerializer, UserSerializer, VerifyOTPSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        send_mail("Your Jobspri OTP", f"OTP: {user.otp_code}", "no-reply@jobspri.com", [user.email])


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email=serializer.validated_data["email"]).first()
        if not user or user.otp_code != serializer.validated_data["otp"]:
            return Response({"detail": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.is_email_verified = True
        user.otp_code = ""
        user.save(update_fields=["is_active", "is_email_verified", "otp_code"])
        return Response({"detail": "Account verified"})


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = RefreshToken.for_user(serializer.validated_data["user"])
        return Response({"access": str(refresh.access_token), "refresh": str(refresh)})


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email=serializer.validated_data["email"]).first()
        if user:
            otp = user.generate_otp()
            send_mail("Reset OTP", f"OTP: {otp}", "no-reply@jobspri.com", [user.email])
        return Response({"detail": "If your email exists, reset instructions were sent."})


class MeView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

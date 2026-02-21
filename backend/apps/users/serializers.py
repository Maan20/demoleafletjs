from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "user_type", "phone")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            password=validated_data["password"],
            user_type=validated_data.get("user_type", "seeker"),
            phone=validated_data.get("phone", ""),
            is_active=False,
        )
        user.generate_otp()
        return user


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs["email"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        attrs["user"] = user
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password", "otp_code", "groups", "user_permissions")

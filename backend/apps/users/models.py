import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.companies.models import Company


class User(AbstractUser):
    USER_TYPE_CHOICES = (("seeker", "Seeker"), ("recruiter", "Recruiter"), ("admin", "Admin"))

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default="seeker")
    headline = models.CharField(max_length=255, blank=True)
    summary = models.TextField(blank=True)
    experience_years = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    current_salary = models.IntegerField(null=True, blank=True)
    expected_salary_min = models.IntegerField(null=True, blank=True)
    expected_salary_max = models.IntegerField(null=True, blank=True)
    notice_period_days = models.IntegerField(null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    resume_data = models.JSONField(default=dict, blank=True)
    resume_pdf = models.FileField(upload_to="resumes/", null=True, blank=True)
    resume_downloads_used = models.IntegerField(default=0)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL, related_name="users")
    otp_code = models.CharField(max_length=6, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def generate_otp(self):
        self.otp_code = f"{random.randint(100000, 999999)}"
        self.save(update_fields=["otp_code"])
        return self.otp_code

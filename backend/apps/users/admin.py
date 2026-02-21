from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("email", "user_type", "is_email_verified", "is_phone_verified", "company")
    search_fields = ("email", "phone", "headline")
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Jobspri", {"fields": ("phone", "user_type", "headline", "company", "is_email_verified", "resume_downloads_used")}),
    )

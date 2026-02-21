from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "industry", "location", "is_verified", "created_at")
    search_fields = ("name", "industry", "location")

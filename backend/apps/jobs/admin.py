from django.contrib import admin
from .models import Job, JobApplication


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "job_type", "experience_level", "is_active", "posted_at")
    search_fields = ("title", "description", "requirements", "company__name", "location")


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("job", "applicant", "status", "applied_at")
    search_fields = ("job__title", "applicant__email", "status")

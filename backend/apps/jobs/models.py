from datetime import timedelta
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from apps.companies.models import Company


class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ("full_time", "Full time"),
        ("part_time", "Part time"),
        ("contract", "Contract"),
        ("internship", "Internship"),
        ("remote", "Remote"),
    )
    EXPERIENCE_CHOICES = (
        ("fresher", "Fresher"),
        ("1-2", "1-2"),
        ("2-5", "2-5"),
        ("5-8", "5-8"),
        ("8+", "8+"),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="jobs_posted")
    description = models.TextField()
    requirements = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)
    location = models.CharField(max_length=255)
    is_remote = models.BooleanField(default=False)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    is_salary_visible = models.BooleanField(default=True)
    skills_required = ArrayField(models.CharField(max_length=50), default=list, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    applications_count = models.PositiveIntegerField(default=0)
    posted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True)
    search_vector = SearchVectorField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.company.name}")
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=30)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    STATUS_CHOICES = (
        ("applied", "Applied"),
        ("viewed", "Viewed"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
        ("hired", "Hired"),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField(blank=True)
    resume_used = models.FileField(upload_to="applications/resumes/", null=True, blank=True)
    applicant_snapshot = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="applied")
    recruiter_notes = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("job", "applicant")

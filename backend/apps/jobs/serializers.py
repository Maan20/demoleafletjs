from django.db.models import F
from rest_framework import serializers
from .models import Job, JobApplication


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = Job
        fields = "__all__"


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = "__all__"
        read_only_fields = ("job", "applicant", "applicant_snapshot", "status")

    def create(self, validated_data):
        job = self.context["job"]
        applicant = self.context["request"].user
        snapshot = {
            "email": applicant.email,
            "headline": applicant.headline,
            "experience_years": str(applicant.experience_years),
            "resume_data": applicant.resume_data,
        }
        obj = JobApplication.objects.create(job=job, applicant=applicant, applicant_snapshot=snapshot, **validated_data)
        Job.objects.filter(id=job.id).update(applications_count=F("applications_count") + 1)
        return obj

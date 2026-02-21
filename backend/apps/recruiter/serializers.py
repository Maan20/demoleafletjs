from rest_framework import serializers
from apps.companies.models import Company
from apps.jobs.models import Job, JobApplication


class RecruiterJobSerializer(serializers.ModelSerializer):
    applications_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ("company", "posted_by", "applications_count")


class RecruiterApplicationSerializer(serializers.ModelSerializer):
    applicant_email = serializers.CharField(source="applicant.email", read_only=True)

    class Meta:
        model = JobApplication
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

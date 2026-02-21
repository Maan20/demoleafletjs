from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.companies.models import Company
from apps.jobs.models import Job, JobApplication
from .permissions import IsCompanyAdmin, IsRecruiter
from .serializers import CompanySerializer, RecruiterApplicationSerializer, RecruiterJobSerializer


class RecruiterJobListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsRecruiter]
    serializer_class = RecruiterJobSerializer

    def get_queryset(self):
        return Job.objects.filter(company=self.request.user.company)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company, posted_by=self.request.user)


class RecruiterJobDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsRecruiter]
    serializer_class = RecruiterJobSerializer
    queryset = Job.objects.all()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=["is_active"])


class RecruiterJobApplicationsView(generics.ListAPIView):
    permission_classes = [IsRecruiter]
    serializer_class = RecruiterApplicationSerializer

    def get_queryset(self):
        qs = JobApplication.objects.filter(job_id=self.kwargs["id"], job__company=self.request.user.company)
        status = self.request.query_params.get("status")
        return qs.filter(status=status) if status else qs


class RecruiterApplicationDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsRecruiter]
    serializer_class = RecruiterApplicationSerializer

    def get_queryset(self):
        return JobApplication.objects.filter(job__company=self.request.user.company)


class RecruiterCompanyView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def get(self, request):
        serializer = CompanySerializer(request.user.company)
        return Response(serializer.data)

    def patch(self, request):
        company = get_object_or_404(Company, id=request.user.company_id)
        self.check_object_permissions(request, company)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_permissions(self):
        perms = super().get_permissions()
        if self.request.method == "PATCH":
            perms.append(IsCompanyAdmin())
        return perms

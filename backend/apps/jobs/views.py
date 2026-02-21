from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Job
from .serializers import JobApplicationSerializer, JobSerializer


class JobListView(generics.ListAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        qs = Job.objects.filter(is_active=True)
        p = self.request.query_params
        if p.get("q"):
            vector = SearchVector("title", "description", "requirements", "skills_required", "company__name")
            qs = qs.annotate(search=vector).filter(search=SearchQuery(p["q"]))
        if p.get("location"):
            qs = qs.filter(location__icontains=p["location"])
        if p.get("job_type"):
            qs = qs.filter(job_type=p["job_type"])
        if p.get("experience_level"):
            qs = qs.filter(experience_level=p["experience_level"])
        if p.get("remote") == "true":
            qs = qs.filter(is_remote=True)
        if p.get("salary_min"):
            qs = qs.filter(Q(salary_min__gte=p["salary_min"]) | Q(salary_max__gte=p["salary_min"]))
        if p.get("skills"):
            for s in p["skills"].split(","):
                qs = qs.filter(skills_required__icontains=s.strip())
        ordering = p.get("ordering", "-posted_at")
        return qs.order_by(ordering)


class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.filter(is_active=True)
    serializer_class = JobSerializer
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        job = self.get_object()
        data = self.get_serializer(job).data
        similar = Job.objects.filter(company=job.company, is_active=True).exclude(id=job.id)[:3]
        data["similar_jobs"] = JobSerializer(similar, many=True).data
        return Response(data)


class ApplyJobView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, slug):
        if request.user.user_type != "seeker":
            raise PermissionDenied("Only seekers can apply")
        job = Job.objects.get(slug=slug, is_active=True)
        serializer = JobApplicationSerializer(data=request.data, context={"request": request, "job": job})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

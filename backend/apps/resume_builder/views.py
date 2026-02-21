from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class ResumeDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(request.user.resume_data or {})

    def put(self, request):
        request.user.resume_data = request.data
        request.user.save(update_fields=["resume_data"])
        return Response(request.user.resume_data)


class ResumeGenerateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        template_id = int(request.data.get("template_id", 1))
        if request.user.resume_downloads_used >= 2:
            return Response({"detail": "Free download limit exceeded"}, status=402)
        html = render_to_string(f"resume_builder/template_{template_id}.html", {"resume": request.user.resume_data or {}})
        request.user.resume_downloads_used += 1
        request.user.save(update_fields=["resume_downloads_used"])
        return HttpResponse(html, content_type="text/html")

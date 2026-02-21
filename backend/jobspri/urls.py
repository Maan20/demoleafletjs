from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.users.urls")),
    path("api/", include("apps.jobs.urls")),
    path("api/", include("apps.recruiter.urls")),
    path("api/", include("apps.resume_builder.urls")),
]

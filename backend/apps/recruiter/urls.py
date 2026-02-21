from django.urls import path
from .views import (
    RecruiterApplicationDetailView,
    RecruiterCompanyView,
    RecruiterJobApplicationsView,
    RecruiterJobDetailView,
    RecruiterJobListCreateView,
)

urlpatterns = [
    path("recruiter/jobs/", RecruiterJobListCreateView.as_view()),
    path("recruiter/jobs/<int:pk>/", RecruiterJobDetailView.as_view()),
    path("recruiter/jobs/<int:id>/applications/", RecruiterJobApplicationsView.as_view()),
    path("recruiter/applications/<int:pk>/", RecruiterApplicationDetailView.as_view()),
    path("recruiter/company/", RecruiterCompanyView.as_view()),
]

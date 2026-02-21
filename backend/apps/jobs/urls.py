from django.urls import path
from .views import ApplyJobView, JobDetailView, JobListView

urlpatterns = [
    path("jobs/", JobListView.as_view()),
    path("jobs/<slug:slug>/", JobDetailView.as_view()),
    path("jobs/<slug:slug>/apply/", ApplyJobView.as_view()),
]

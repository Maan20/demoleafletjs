from django.urls import path
from .views import ResumeDataView, ResumeGenerateView

urlpatterns = [
    path("resume/data/", ResumeDataView.as_view()),
    path("resume/generate/", ResumeGenerateView.as_view()),
]

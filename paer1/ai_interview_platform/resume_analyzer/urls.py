# resume_analyzer/urls.py
from django.urls import path
from . import views

app_name = 'resume_analyzer'

urlpatterns = [
    # This view will handle both tools, we pass data to distinguish them
    path('resume-analyzer/', views.analyzer_view, {'page_type': 'analyzer'}, name='analyzer'),
    path('ats-checker/', views.analyzer_view, {'page_type': 'ats_checker'}, name='ats_checker'),
]
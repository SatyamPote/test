# ai_interview_platform/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import the new homepage view
from .views import homepage_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # Homepage URL
    path('', homepage_view, name='homepage'),
    # URLs for the interview app
    path('interviews/', include('interviews.urls')),
    # URLs for the new resume analyzer app
    path('tools/', include('resume_analyzer.urls')),
]

# This is important for serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
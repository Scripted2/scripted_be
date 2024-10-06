from django.urls import path
from .views import VideoSearchView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/videos/search/', VideoSearchView.as_view(), name='video-search'),  # URL for searching videos
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Setting to set the base url of videos
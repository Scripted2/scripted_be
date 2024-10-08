from rest_framework.routers import DefaultRouter

from video.views import VideoView

videos_router = DefaultRouter()
videos_router.register(r'video', VideoView, basename='video')
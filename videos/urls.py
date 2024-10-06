from rest_framework.routers import DefaultRouter

from videos.views import VideoSearchView

videos_router = DefaultRouter()
videos_router.register(r'video', VideoSearchView, basename='video')
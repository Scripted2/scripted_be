from rest_framework.routers import DefaultRouter

from users.views import SignUpViewSet

users_router = DefaultRouter()
users_router.register(r'signup', SignUpViewSet, basename='signup')

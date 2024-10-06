from rest_framework.routers import DefaultRouter

from users.views import SignUpViewSet, CategoriesViewSet

users_router = DefaultRouter()
users_router.register(r'signup', SignUpViewSet, basename='signup')
users_router.register(r'category', CategoriesViewSet, basename='category')

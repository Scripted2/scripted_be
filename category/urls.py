from rest_framework.routers import DefaultRouter

from category.views import CategoriesViewSet

category_router = DefaultRouter()
category_router.register(r'category', CategoriesViewSet, basename='category')

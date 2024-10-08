from rest_framework.routers import DefaultRouter

from category.views import CategoriesViewSet

categories_router = DefaultRouter()
categories_router.register(r'categories', CategoriesViewSet, basename='categories')

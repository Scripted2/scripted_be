from rest_framework.routers import DefaultRouter

from user.views import SignUpViewSet, CodeSnippetViewSet

users_router = DefaultRouter()
users_router.register(r'signup', SignUpViewSet, basename='signup')

snippets_router = DefaultRouter()
snippets_router.register(r'snippets',CodeSnippetViewSet, basename='snippet')

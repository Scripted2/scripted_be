from rest_framework.routers import DefaultRouter

from comments.views import CommentView

comments_router = DefaultRouter()
comments_router.register(r'comment', CommentView, basename='comment')

from rest_framework.routers import DefaultRouter

from comment.views import CommentView

comments_router = DefaultRouter()
comments_router.register(r'comments', CommentView, basename='comments')

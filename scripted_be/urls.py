from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from comment.urls import comments_router
from user.urls import users_router, snippets_router
from user.views import CustomTokenObtainPairView
from video.urls import videos_router

from category.urls import categories_router

router = routers.SimpleRouter(trailing_slash=False)
router.registry.extend(users_router.registry)
router.registry.extend(videos_router.registry)
router.registry.extend(comments_router.registry)
router.registry.extend(categories_router.registry)
router.registry.extend(snippets_router.registry)

api_urlpatterns = [
    path('', include(router.urls)),
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(api_urlpatterns)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

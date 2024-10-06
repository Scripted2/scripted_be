from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from users.urls import users_router

router = routers.SimpleRouter(trailing_slash=False)
router.registry.extend(users_router.registry)

api_urlpatterns = [
    path('', include(router.urls)),
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', CustomTokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(api_urlpatterns)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

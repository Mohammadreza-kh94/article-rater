from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import UserViewSet, ArticleViewSet, RatingViewSet, RegisterView

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("articles", ArticleViewSet, basename="article")
router.register("ratings", RatingViewSet, basename="rating")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    # Auth Endpoints
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

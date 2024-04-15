from django.urls import path, include

from .views import CatViewSet, OwnerViewSet, AchievementViewSet, APICat
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('cats', CatViewSet, basename='cats')
router.register(r'owner', OwnerViewSet, basename='owners')
router.register(r'achievement', AchievementViewSet, basename='achievements')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('cats2/', APICat.as_view()),
]

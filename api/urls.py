from django.urls import path, include

from .views import cat_list, APICat, CatList, CatDetail, CatViewSet

from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register('cats_v', CatViewSet, basename='cats_v')

urlpatterns = [
    path('', include(router.urls)),
    path('cats/', cat_list),
    path('cats_class/', APICat.as_view()),
    path('cats_g/', CatList.as_view()),
    path('cats_g/<int:pk>/', CatDetail.as_view()),
    ]

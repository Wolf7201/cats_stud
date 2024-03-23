from django.urls import path

from .views import cat_list

urlpatterns = [
    path('cats/', cat_list),
]

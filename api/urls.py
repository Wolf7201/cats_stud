from django.urls import path

from .views import cat_list, hello

urlpatterns = [
    path('cats/', cat_list),
    path('hello/', hello),
]

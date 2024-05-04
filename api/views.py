from django.shortcuts import get_object_or_404
from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import OwnerOrReadOnly
from .models import Cat, User, Achievement
from .serializers import CatSerializer, OwnerSerializer, AchievementSerializer
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from .paginations import OwnersPagination

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


# View-функция cat_list() будет обрабатывать только запросы GET и POST,
# запросы других типов будут отклонены,
# так что в теле функции их можно не обрабатывать
@api_view(['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def cat_list(request):
    if request.method == 'POST':
        serializer = CatSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH' or 'PUT':
        cat_id = request.data.get('id')

        if not cat_id:
            return Response({'error': 'id is required'}, status=status.HTTP_400_BAD_REQUEST)

        cat = get_object_or_404(Cat, id=cat_id)
        if request.method == 'PATCH':
            serializer = CatSerializer(cat, data=request.data, partial=True)
        else:
            serializer = CatSerializer(cat, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        cat_id = request.data.get('id')
        if not cat_id:
            return Response({'error': 'id is required'}, status=status.HTTP_400_BAD_REQUEST)
        cat = get_object_or_404(Cat, id=cat_id)
        cat.delete()
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)

    cats = Cat.objects.all()
    serializer = CatSerializer(cats, many=True)
    return Response(serializer.data)


class APICat(APIView):
    def get(self, request):
        print(request.user.id)
        cats = Cat.objects.all()
        serializer = CatSerializer(cats, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CatList(generics.ListCreateAPIView):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer


class CatDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['color', 'birth_year']
    search_fields = ['^name']
    ordering_fields = ('name', 'birth_year')
    ordering = ('birth_year',)
    # http://127.0.0.1:8000/cats/


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = OwnerSerializer
    pagination_class = OwnersPagination

    # GET http://127.0.0.1:8000/cats/?limit=2&offset=4


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer

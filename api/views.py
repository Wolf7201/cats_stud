from django.shortcuts import get_object_or_404
from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cat
from .serializers import CatSerializer


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


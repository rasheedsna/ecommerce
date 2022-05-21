from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . models import Category, Product
from . serializers import ProductSerializer, CategorySerializer


@api_view(['GET'])
def all_categories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def all_products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


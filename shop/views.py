from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Product
from .serializers import ProductSerializer, CategorySerializer
from .permissions import AuthorisedEditOnly


class AllCategories(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditCategory(APIView):
    def get(self, request, category_id):
        try:
            category = Category.objects.get(_id=category_id)
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'msg': 'requested resources does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, category_id):
        try:
            category = Category.objects.get(_id=category_id)
            serializer = CategorySerializer(category, data=request.data, partial=True)
        except ObjectDoesNotExist:
            return Response({'msg': 'requested resources does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id):
        try:
            category = Category.objects.get(_id=category_id)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({'msg': 'requested resources does not exist'}, status=status.HTTP_404_NOT_FOUND)


class AllProducts(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditProduct(APIView):
    permission_classes = [AuthorisedEditOnly]

    def get(self, request, product_id):
        try:
            product = Product.objects.get(_id=product_id)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'msg': 'requested resources does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, product_id):
        try:
            product = Product.objects.get(_id=product_id)
            serializer = ProductSerializer(product, data=request.data, partial=True)
        except ObjectDoesNotExist:
            return Response({'msg': 'requested resources does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        try:
            product = Product.objects.get(_id=product_id)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({'msg': 'requested resources does not exist'}, status=status.HTTP_404_NOT_FOUND)



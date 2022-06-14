from rest_framework import generics, filters
from shop.models import Category
from shop.serializers import CategorySerializer


class CategorySearchAPIView(generics.ListCreateAPIView):
    search_fields = ['parent']
    filter_backends = (filters.SearchFilter,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

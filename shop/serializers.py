from rest_framework import serializers
from . models import Category, Product, SubCategory, Type


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

    # def to_representation(self, instance):
    #     return '%s' % instance.children


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.StringRelatedField(many=True)

    class Meta:
        model = Category
        fields = ['_id', 'parent', 'type', 'icon', 'children']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['type'] = TypeSerializer(instance.type).data['type']
        return response


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['children'] = SubCategorySerializer(instance.children).data['children']
        response['parent'] = CategorySerializer(instance.parent).data['parent']
        response['type'] = TypeSerializer(instance.parent.type).data['type']
        return response
    # def create(self, validated_data):

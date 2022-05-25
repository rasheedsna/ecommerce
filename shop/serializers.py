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


class ChildrenListingField(serializers.RelatedField):
    def to_representation(self, instance):
        return '%s' % instance.children

    def to_internal_value(self, data):
        return data


class CategorySerializer(serializers.ModelSerializer):
    # children = serializers.StringRelatedField(many=True, allow_null=True)
    children = ChildrenListingField(many=True, queryset=Category.objects.all())

    class Meta:
        model = Category
        fields = ['_id', 'parent', 'type', 'icon', 'children']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['type'] = TypeSerializer(instance.type).data['type']
        return response

    def create(self, validated_data):
        parent = validated_data.get('parent')
        icon = validated_data.get('icon')
        product_type = Type.objects.get(type=validated_data['type'])
        children = validated_data.get('children')

        category = Category.objects.create(
            parent=parent,
            icon=icon,
            type=product_type,
        )
        category.save()

        parent_for_sub_category = category
        for item in children:
            sub_category = SubCategory.objects.create(
                children=item,
                parent=parent_for_sub_category,
            )
            sub_category.save()

        return category


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

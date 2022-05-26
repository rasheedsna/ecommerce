from rest_framework import serializers
from .models import Category, Product, SubCategory, Type, Tag


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

    def to_internal_value(self, data):
        return data

    def create(self, validated_data):
        parent = validated_data.get('parent')
        icon = validated_data.get('icon')
        product_type = Type.objects.get(id=validated_data['type'])
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


class TagListingField(serializers.RelatedField):
    def to_representation(self, instance):
        return '%s' % instance.tag

    def to_internal_value(self, data):
        return data


class ProductSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(allow_unicode=False, max_length=200, read_only=True)
    tag = TagListingField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Product
        fields = ['_id', 'title', 'description', 'image', 'SKU', 'createdAt', 'updatedAt', 'status', 'quantity',
                  'originalPrice', 'price', 'slug', 'unit', 'parent', 'children', 'tag']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['children'] = SubCategorySerializer(instance.children).data['children']
        response['parent'] = CategorySerializer(instance.parent).data['parent']
        response['type'] = TypeSerializer(instance.parent.type).data['type']
        return response

    def to_internal_value(self, data):
        return data

    def create(self, validated_data):
        print(validated_data)
        title = validated_data.get('title')
        description = validated_data.get('description')
        image = validated_data.get('image')
        sku = validated_data.get('SKU')
        quantity = validated_data.get('quantity')
        unit = validated_data.get('unit')
        price = validated_data.get('price')
        original_price = validated_data.get('originalPrice')
        parent = Category.objects.get(_id=validated_data.get('parent'))
        children = SubCategory.objects.get(pk=validated_data.get('children'))
        tags = validated_data.get('tag')

        product = Product.objects.create(
            title=title,
            description=description,
            image=image,
            SKU=sku,
            quantity=quantity,
            unit=unit,
            price=price,
            originalPrice=original_price,
            parent=parent,
            children=children,
        )
        product.save()

        product_for_tag = product
        for item in tags:
            tag = Tag.objects.create(
                tag=item,
                product=product_for_tag,
            )
            tag.save()

        return product

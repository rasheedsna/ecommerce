from django.core.exceptions import ObjectDoesNotExist
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


class ChildrenListingField(serializers.RelatedField):
    def to_representation(self, instance):
        return '%s' % instance.children

    def to_internal_value(self, data):
        return data


class CategorySerializer(serializers.ModelSerializer):
    children = ChildrenListingField(many=True, queryset=Category.objects.all())

    class Meta:
        model = Category
        fields = ['_id', 'parent', 'type', 'icon', 'children']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['type'] = TypeSerializer(instance.type).data['type']
        return response

    def create(self, validated_data):
        print(validated_data)
        parent = validated_data.get('parent')
        icon = validated_data.get('icon')
        product_type = validated_data.get('type')
        children = validated_data.get('children')

        category = Category.objects.create(
            parent=parent,
            icon=icon,
            type=product_type,
        )
        category.save()

        for item in children:
            sub_category = SubCategory.objects.create(
                children=item,
                parent=category,
            )
            sub_category.save()

        return category

    def update(self, instance, validated_data):
        instance.parent = validated_data.get('parent', instance.parent)
        instance.icon = validated_data.get('icon', instance.icon)
        instance.type = validated_data.get('type', instance.type)
        instance.save()

        children = validated_data.get('children')
        if children is not None:
            sub_categories = SubCategory.objects.filter(parent=instance)
            for sub_cat in sub_categories:
                sub_cat.delete()

            for item in children:
                sub_category = SubCategory.objects.create(
                    children=item,
                    parent=instance,
                )
                sub_category.save()

        return instance


class TagListingField(serializers.RelatedField):
    def to_representation(self, instance):
        return '%s' % instance.tag

    def to_internal_value(self, data):
        return data


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_empty_file=True, allow_null=True, required=False)
    slug = serializers.SlugField(allow_unicode=False, max_length=200, read_only=True)
    tags = TagListingField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Product
        fields = ['_id', 'title', 'description', 'image', 'SKU', 'createdAt', 'updatedAt', 'status', 'quantity',
                  'originalPrice', 'price', 'discount', 'slug', 'unit', 'parent', 'children', 'tags']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['children'] = SubCategorySerializer(instance.children).data['children']
        response['parent'] = CategorySerializer(instance.parent).data['parent']
        response['type'] = TypeSerializer(instance.parent.type).data['type']
        return response

    def create(self, validated_data):
        title = validated_data.get('title')
        description = validated_data.get('description')
        image = validated_data.get('image')
        sku = validated_data.get('SKU')
        quantity = validated_data.get('quantity')
        unit = validated_data.get('unit')
        price = validated_data.get('price')
        original_price = validated_data.get('originalPrice')
        parent = validated_data.get('parent')
        children = validated_data.get('children')
        tags = validated_data.get('tags')

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

        if tags is not None:
            for item in tags:
                try:
                    tag = Tag.objects.get(tag=item)
                    tag.product.add(product)
                except ObjectDoesNotExist:
                    tag = Tag.objects.create(
                        tag=item,
                    )
                    tag.save()
                    tag.product.add(product)

        return product

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.SKU = validated_data.get('SKU', instance.SKU)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.originalPrice = validated_data.get('originalPrice', instance.originalPrice)
        instance.price = validated_data.get('price', instance.price)
        instance.unit = validated_data.get('unit', instance.unit)
        instance.children = validated_data.get('children', instance.children)
        instance.parent = validated_data.get('parent', instance.parent)
        instance.save()

        tags = validated_data.get('tags')

        if tags is not None:
            for item in tags:
                try:
                    tag = Tag.objects.get(tag=item)
                    tag.product.add(instance)
                except ObjectDoesNotExist:
                    tag = Tag.objects.create(
                        tag=item,
                    )
                tag.save()
                tag.product.add(instance)
        return instance

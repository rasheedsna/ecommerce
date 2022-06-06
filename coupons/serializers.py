import random
from rest_framework import serializers
from .models import Coupons
from shop.serializers import TypeSerializer


def generate_coupon_code(title, discount):
    start = str(title).split()[0].upper()
    end = str(int(discount))
    code = start[0:4] + end
    while Coupons.objects.filter(couponCode=code).exists():
        mix = str(random.randrange(0, 100))
        code = start[0:4] + mix + end
    return code


class CouponSerializer(serializers.ModelSerializer):
    couponCode = serializers.CharField(max_length=10, required=False)

    class Meta:
        model = Coupons
        fields = ['_id', 'createdAt', 'updatedAt', 'discountPercentage', 'title', 'couponCode', 'endTime',
                  'minimumAmount', 'logo', 'productType']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['productType'] = TypeSerializer(instance.productType).data.get('type')
        return response

    def create(self, validated_data):
        coupon_code = generate_coupon_code(validated_data.get('title'), validated_data.get('discountPercentage'))
        coupon = Coupons.objects.create(
            **validated_data
        )
        coupon.couponCode = coupon_code
        coupon.save()

        return coupon

    def update(self, instance, validated_data):
        new_title = validated_data.get('title', instance.title)
        new_discount_percentage = validated_data.get('discountPercentage', instance.discountPercentage)
        if instance.title != new_title or instance.discountPercentage != new_discount_percentage:
            instance.couponCode = generate_coupon_code(new_title, new_discount_percentage)

        instance.title = new_title
        instance.discountPercentage = new_discount_percentage
        instance.endTime = validated_data.get('endTime', instance.endTime)
        instance.minimumAmount = validated_data.get('minimumAmount', instance.minimumAmount)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.productType = validated_data.get('productType', instance.productType)
        instance.save()

        return instance


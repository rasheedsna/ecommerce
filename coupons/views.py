from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Coupons
from .serializers import CouponSerializer


@api_view(['GET', 'POST'])
def coupons(request):
    if request.method == 'GET':
        all_coupons = Coupons.objects.all()
        serializer = CouponSerializer(all_coupons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = CouponSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def edit_coupons(request, coupon_id):
    if request.method == 'GET':
        coupon = Coupons.objects.get(_id=coupon_id)
        serializer = CouponSerializer(coupon)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        coupon = Coupons.objects.get(_id=coupon_id)
        serializer = CouponSerializer(coupon, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        coupon = Coupons.objects.get(_id=coupon_id)
        coupon.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


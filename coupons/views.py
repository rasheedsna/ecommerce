from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Coupons
from .serializers import CouponSerializer


class AllCouponsView(APIView):
    def get(self, request):
        all_coupons = Coupons.objects.all()
        serializer = CouponSerializer(all_coupons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CouponSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditCoupons(APIView):
    def get(self, request, coupon_id):
        try:
            coupon = Coupons.objects.get(_id=coupon_id)
            serializer = CouponSerializer(coupon)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'msg': 'requested resources does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, coupon_id):
        try:
            coupon = Coupons.objects.get(_id=coupon_id)
            serializer = CouponSerializer(coupon, data=request.data, partial=True)
        except ObjectDoesNotExist:
            return Response({'msg': 'requested resources does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, coupon_id):
        try:
            coupon = Coupons.objects.get(_id=coupon_id)
            coupon.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({'msg': 'requested resources does not exist'}, status=status.HTTP_404_NOT_FOUND)





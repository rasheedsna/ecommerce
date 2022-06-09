from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . models import UserProfile
from . serializers import UserProfileSerializer, AdminUserSerializer
from .permissions import AuthenticatedUserOrAdminViewOnly, AuthenticatedAdminUserOrAdminViewOnly


class UserAccounts(APIView):
    def get(self, request):
        users = UserProfile.objects.filter(is_staff=False)
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditUserAccounts(APIView):
    permission_classes = [AuthenticatedUserOrAdminViewOnly]

    def get(self, request, user_id):
        try:
            user = UserProfile.objects.get(_id=user_id, is_staff=False)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'msg': 'requested resources does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, user_id):
        try:
            user = UserProfile.objects.get(_id=user_id)
            serializer = UserProfileSerializer(user, data=request.data, partial=True)
        except ObjectDoesNotExist:
            return Response({'msg': 'requested resources does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        try:
            user = UserProfile.objects.get(_id=user_id)
            user.is_active = False
            user.save()
            return Response({'msg': 'this account has been deactivated'}, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({'msg': 'requested resources does not exist'}, status=status.HTTP_404_NOT_FOUND)


class AdminAccounts(APIView):
    def get(self, request):
        users = UserProfile.objects.filter(is_staff=True)
        serializer = AdminUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AdminUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditAdminUserAccounts(APIView):
    permission_classes = [AuthenticatedAdminUserOrAdminViewOnly]

    def get(self, request, user_id):
        try:
            user = UserProfile.objects.get(_id=user_id, is_staff=True)
            serializer = AdminUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'msg': 'requested resources does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, user_id):
        try:
            user = UserProfile.objects.get(_id=user_id, is_staff=True)
            serializer = AdminUserSerializer(user, data=request.data, partial=True)
        except ObjectDoesNotExist:
            return Response({'msg': 'requested resources does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        try:
            user = UserProfile.objects.get(_id=user_id)
            user.is_active = False
            user.save()
            return Response({'msg': 'this account has been deactivated'}, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({'msg': 'requested resources does not exist'}, status=status.HTTP_404_NOT_FOUND)



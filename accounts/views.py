from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . models import UserProfile
from . serializers import UserProfileSerializer, AdminUserSerializer


@api_view(['GET', 'POST'])
def user_accounts(request):
    if request.method == 'GET':
        users = UserProfile.objects.filter(is_staff=False)
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = UserProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def edit_user_accounts(request, user_id):
    if request.method == 'PATCH':
        users = UserProfile.objects.get(_id=user_id)
        serializer = UserProfileSerializer(users, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def admin_accounts(request):
    if request.method == 'GET':
        users = UserProfile.objects.filter(is_staff=True)
        serializer = AdminUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = AdminUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def edit_admin_accounts(request, user_id):
    if request.method == 'PATCH':
        users = UserProfile.objects.filter(_id=user_id, is_staff=True)
        serializer = AdminUserSerializer(users, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

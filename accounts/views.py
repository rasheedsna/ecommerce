from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . models import UserProfile, Roll
from . serializers import UserProfileSerializer


@api_view(['GET'])
def user_accounts(request):
    if request.method == 'GET':
        users = UserProfile.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

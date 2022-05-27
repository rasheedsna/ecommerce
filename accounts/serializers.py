from rest_framework import serializers
from . models import UserProfile, Role


class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['_id', 'name', 'phone', 'password', 'email', 'image', 'address', 'createdAt']

    # def update(self, instance, validated_data):
    #     instance.address = validated_data.get('address')
    #     return instance


class AdminRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class AdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['_id', 'name', 'phone', 'password', 'email', 'image', 'createdAt', 'updatedAt', 'joiningDate', 'role']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['role'] = AdminRoleSerializer(instance.role).data.get('role')
        return response

    def to_internal_value(self, data):
        return data

    # def create(self, validated_data):

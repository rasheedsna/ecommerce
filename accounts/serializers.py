from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import Group


class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['_id', 'name', 'phone', 'password', 'email', 'image', 'address', 'createdAt']

    def create(self, validated_data):
        phone = validated_data.get('phone')
        name = validated_data.get('name')
        password = validated_data.get('password')
        group = Group.objects.get(name='Customer')
        user = UserProfile.objects.create_user(password=password, phone=phone, name=name)
        user.groups.add(group)
        user.save()

        return user

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.image = validated_data.get('image', instance.image)
        instance.address = validated_data.get('address', instance.address)

        instance.save()

        return instance


class AdminGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class AdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(write_only=True, required=True, max_length=50)

    class Meta:
        model = UserProfile
        fields = ['_id', 'name', 'phone', 'password', 'email', 'image', 'createdAt', 'updatedAt', 'joiningDate', 'role']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['role'] = AdminGroupSerializer(instance.groups.all(), many=True).data[0].get('name')
        return response

    def create(self, validated_data):
        phone = validated_data.get('phone')
        name = validated_data.get('name')
        password = validated_data.get('password')
        email = validated_data.get('email')
        image = validated_data.get('image')
        joining_date = validated_data.get('joiningDate')
        role = Group.objects.get(id=validated_data.get('role'))
        print(role)

        user = UserProfile.objects.create_user(
            password=password,
            phone=phone,
            name=name,
            email=email,
            image=image,
            joiningDate=joining_date,
        )
        user.is_staff = True
        user.groups.add(role)
        user.save()

        return user

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.image = validated_data.get('image', instance.image)
        role = Group.objects.get(id=validated_data.get('role'))
        password = validated_data.get('password')

        if password is not None:
            instance.set_password(password)

        if role not in instance.groups.all():
            instance.groups.clear()
            instance.groups.add(role)
        instance.save()

        return instance




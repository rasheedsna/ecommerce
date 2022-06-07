from rest_framework import serializers
from . models import UserProfile, Role


class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['_id', 'name', 'phone', 'password', 'email', 'image', 'address', 'createdAt']

    def create(self, validated_data):
        phone = validated_data.get('phone')
        name = validated_data.get('name')
        password = validated_data.get('password')

        user = UserProfile.objects.create_user(password=password, phone=phone, name=name)
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

    def create(self, validated_data):
        phone = validated_data.get('phone')
        name = validated_data.get('name')
        password = validated_data.get('password')
        email = validated_data.get('email')
        image = validated_data.get('image')
        joining_date = validated_data.get('joiningDate')
        role = validated_data.get('role')
        print(role)

        user = UserProfile.objects.create_user(
            password=password,
            phone=phone,
            name=name,
            email=email,
            image=image,
            joiningDate=joining_date,
            role=role
        )
        user.is_staff = True
        user.save()

        return user

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.image = validated_data.get('image', instance.image)
        instance.role = validated_data.get('role', instance.role)
        password = validated_data.get('password')

        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance


class UserListingField(serializers.RelatedField):
    def to_representation(self, instance):
        return '%s' % instance.name

    def to_internal_value(self, data):
        return data





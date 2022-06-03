from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
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

        # password = validated_data.get('password')
        #
        # if password is not None:
        #     instance.set_password(password)
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


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20, write_only=True)
    password = serializers.CharField(max_length=100, write_only=True)
    user = UserListingField(read_only=True)
    refresh = serializers.CharField(max_length=300, read_only=True)
    access = serializers.CharField(max_length=300, read_only=True)

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')

        if phone and password:
            user = authenticate(phone=phone, password=password)
            if user is not None:
                data['user'] = user
                refresh = RefreshToken.for_user(user)
                data['refresh'] = str(refresh)
                data['access'] = str(refresh.access_token)
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'provide both credentials'
            raise serializers.ValidationError(msg, code='authorization')
        return data


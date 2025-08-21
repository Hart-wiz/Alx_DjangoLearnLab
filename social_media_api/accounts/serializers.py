# # accounts/serializers.py
# from django.contrib.auth import authenticate
# from django.contrib.auth.password_validation import validate_password
# from rest_framework import serializers
# from rest_framework.authtoken.models import Token
# from .models import User


# class UserSerializer(serializers.ModelSerializer):
#     followers_count = serializers.IntegerField(source='followers.count', read_only=True)
#     following_count = serializers.IntegerField(source='following.count', read_only=True)

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'bio', 'profile_picture',
#                   'followers_count', 'following_count')

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password', 'bio', 'profile_picture')

#     def validate_password(self, value):
#         validate_password(value)
#         return value

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = User(**validated_data)
#         user.set_password(password)
#         user.save()
#         # create token on signup
#         Token.objects.create(user=user)
#         return user

# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, attrs):
#         user = authenticate(username=attrs.get('username'), password=attrs.get('password'))
#         if not user:
#             raise serializers.ValidationError('Invalid credentials.')
#         attrs['user'] = user
#         return attrs
# class ProfileUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('bio', 'profile_picture', 'email')  # limit what can be edited
# accounts/serializers.py
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'bio', 'profile_picture',
            'followers_count', 'following_count'
        )
        read_only_fields = ('id', 'followers_count', 'following_count')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'bio', 'profile_picture')

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        # IMPORTANT: use get_user_model().objects.create_user to satisfy tests & hash password
        password = validated_data.pop('password')
        user = get_user_model().objects.create_user(password=password, **validated_data)
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        user = authenticate(username=attrs.get('username'), password=attrs.get('password'))
        if not user:
            raise serializers.ValidationError('Invalid credentials.')
        attrs['user'] = user
        return attrs


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('bio', 'profile_picture', 'email')  # limit what can be updated

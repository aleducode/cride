"""Users Serializers."""

# Django
from django.contrib.auth import password_validation, authenticate
# Django Rest Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator
from rest_framework.authtoken.models import Token
# Model
from cride.users.models import User, Profile


class UserModelSerializaer(serializers.ModelSerializer):
    """User model serializer"""

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email'
        )


class UserSignUpSerializer(serializers.Serializer):
    """Users signup serializer

    Handle sign up data validation and user/profile creation
    """
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.SlugField(
        max_length=14,
        min_length=4,
        # unique field respect circles objecs
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    # Phone number
    phone_regex = RegexValidator(
        regex='\+?1?\d{9,15}$',
        message='phone number must be entered in the format +99999999999'
    )
    phone_number = serializers.CharField(
        validators=[phone_regex]
    )
    # Password
    password = serializers.CharField(max_length=14, min_length=4)
    password_confirmation = serializers.CharField(max_length=14, min_length=4)

    # Name
    first_name = serializers.CharField(min_length=1)
    last_name = serializers.CharField(min_length=1)

    def validate(self, data):
        """Verify password match"""
        passwd = data.get('password')
        passwd_conf = data.get('password_confirmation')
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords does not match.")
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """Handle user and profile creation"""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_verified=False)
        profile = Profile.objects.create(user=user)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Users login Serializer.

    Handle login request data.
    """
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    def validate(self, data):
        """Check credentials"""
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credential')
        if not user.is_verified:
            raise serializers.ValidationError("User need validate account. Account is not active yet.")
        self.context['user'] = user
        return data

    def create(self, data):
        """Generate or retrieve new token"""
        # Token is one to one field with user
        token, created = Token.objects.get_or_create(user=self.context.get('user'))
        return self.context['user'], token.key

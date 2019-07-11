"""Users Serializers."""

# Django
from django.contrib.auth import password_validation, authenticate
from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

# Django Rest Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator
from rest_framework.authtoken.models import Token

# Model
from cride.users.models import User, Profile

# Serializer
from cride.users.serializers.profiles import ProfileModelSerializer

# Utilities
from datetime import timedelta
import jwt


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer"""

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile'
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
        user = User.objects.create_user(**data, is_verified=False, is_client=True)
        profile = Profile.objects.create(user=user)
        self.send_confirmation_email(user)
        return user

    def send_confirmation_email(self, user):
        """Send verification link to given user"""
        verification_token = self.gen_verification_token(user)
        subject = 'Welcome @{}! Verify your account to start using comparte Ride.'.format(user.username)
        from_email = 'Comparte Ride <noreply@comparteride.com>'
        content = render_to_string(
            'email/users/account_verification.html',
            {'token': verification_token, 'user': user})
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()

    def gen_verification_token(self, user):
        """Create JWT token that the user can use to verify its account"""
        expiration_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            # UTC format
            'exp': int(expiration_date.timestamp()),
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token.decode()


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


class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer"""
    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid"""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')
        self.context['payload'] = payload

        return data

    def save(self):
        """Update user's verified status"""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()

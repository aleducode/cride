"""User model"""

# django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# utils
from cride.utils.models import CRideModel


class User(CRideModel, AbstractUser):
    """User model.
    Extend from Django abstract user, change the username field to email
    and add some extra info
    """
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exist',
        }


    )
    phone_regex = RegexValidator(
        regex='\+?1?\d{9,15}$',
        message='phone number must be entered in the format +99999999999'
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    is_client = models.BooleanField(
        'client',
        default=True,
    )
    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text='set to true when address email have verified'
    )

    def __str__(self):
        """Return username"""
        return self.username

    def get_short_name(self):
        """Return username"""
        return self.username

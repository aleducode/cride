"""Circle model"""

# Django
from django.db import models

# Utilities
from cride.utils.models import CRideModel


class Circle(CRideModel):
    """circle model
    A circle is a private group where rides are offered and taken
    by its members. To join a circle a user must be receive an unique
    invitation code from an existing circle member
    """

    name = models.CharField('circle name', max_length=140)
    slug_name = models.SlugField(unique=True, max_length=40)

    about = models.CharField('circle description', max_length=255)
    picture = models.ImageField(upload_to='circles/picture', blank=True, null=True)

    members = models.ManyToManyField(
        'users.User', through='circles.Membership',
        through_fields=('circle', 'user')
        )

    # stats
    rides_offered = models.PositiveIntegerField(default=0)
    rides_taken = models.PositiveIntegerField(default=0)

    verified = models.BooleanField(
        'verified circle',
        default=0,
        help_text='verified circles are also known as official communities.'
    )

    is_public = models.BooleanField(
        default=True,
        help_text='public circles ar listed in the main page so everyone know about their existance.'
    )

    is_limited = models.BooleanField(
        'limited',
        default=0,
        help_text='limited circles can grow up to a fixed number of members'
    )
    members_limit = models.PositiveIntegerField(
        default=0,
        help_text='If circle is limited, this will be the limit of the number of members'

    )

    def __str__(self):
        """Return circles name"""
        return self.name

    # override class meta from Cridemodel
    class Meta(CRideModel.Meta):
        ordering = ['-rides_taken', '-rides_offered']

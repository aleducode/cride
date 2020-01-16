"""Membership model."""

# Django
from django.db import models

# Utilities
from cride.utils.models import CRideModel


class Membership(CRideModel):
    """Membership model.

    is the table thats holds the relationship
    between a user and a circle.
    """

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    circle = models.ForeignKey('circles.Circle', on_delete=models.CASCADE)

    is_admin = models.BooleanField(
        default=True,
        help_text='circle admins can update the circles data and manage its members.'
    )
    used_invitations = models.PositiveSmallIntegerField(default=0)
    remaining_invitations = models.PositiveSmallIntegerField(default=0)
    invited_by = models.ForeignKey(
        'users.User',
        null=True,
        on_delete=models.SET_NULL,
        related_name='invited_by'
    )

    # stats
    rides_offered = models.PositiveIntegerField(default=0)
    rides_taken = models.PositiveIntegerField(default=0)

    # Status
    is_active = models.BooleanField(
        default=True,
        help_text='only active user are allow to interact in the circle.'
    )

    def __str__(self):
        """Return username and circle."""
        return '@{} at #{}'.format(self.user.username, self.circle.slug_name)

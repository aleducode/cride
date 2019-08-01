"""Invitations test."""

# Django
from django.test import TestCase

# Model
from cride.circles.models import Invitation, Circle
from cride.users.models import User


class InvitationsManagerTestCase(TestCase):
    """Invitations manager test case."""

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create_user(
            first_name='Test',
            last_name='Test 2',
            email='test@a.com',
            username='test',
            password='testpass'
        )
        self.circle = Circle.objects.create(
            name='facultad de ciencias',
            slug_name='fciencias',
            about='fciencias',
            verified=True
        )

    def test_code_generation(self):
        """Random codes should be generated automaticlly."""
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle
        )
        self.assertIsNotNone(invitation.code)
"""Invitations test."""

# Django
from django.test import TestCase

# Model
from cride.circles.models import Invitation, Circle, Membership
from cride.users.models import User

# Django Rest Framework
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


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


class MemberInvitationsAPITestCase(APITestCase):
    """Member invitation API test case."""

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
        self.membership = Membership.objects.create(
            user=self.user,
            circle=self.circle,
            remaining_invitations=10
        )
        # Auth
        self.token = Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token))

        # URL
        self.url = '/circles/{}/members/{}/invitations/'.format(
            self.circle.slug_name,
            self.user.username
        )

    def test_response_success(self):
        """Verify request succees."""
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_invitation_creation(self):
        """Verify invitations are generated if none exist previously."""
        # Invitations in DB must be 0
        self.assertEqual(Invitation.objects.count(), 0)

        # Call member invitations Url
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

        # Verify new invitations where created
        invitations = Invitation.objects.filter(issued_by=self.user)
        self.assertEqual(invitations.count(), self.membership.remaining_invitations)
        for invitation in invitations:
            self.assertIn(invitation.code, request.data['invitations'])
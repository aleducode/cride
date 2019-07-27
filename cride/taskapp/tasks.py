"""Celery Tasks."""

# Django
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.conf import settings

# Celery
from celery.decorators import task, periodic_task

# Models
from cride.users.models import User
from cride.rides.models import Ride

# Utilities
from datetime import timedelta
import jwt


def gen_verification_token(user):
        """Create JWT token that the user can use to verify its account."""
        expiration_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            # UTC format
            'exp': int(expiration_date.timestamp()),
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token.decode()


@task(name='send_confirmation_email', max_retries=3)
def send_confirmation_email(user_pk):
    """Send verification link to given user."""
    user = User.objects.get(pk=user_pk)
    verification_token = gen_verification_token(user)
    subject = 'Welcome @{}! Verify your account to start using comparte Ride.'.format(user.username)
    from_email = 'Comparte Ride <noreply@comparteride.com>'
    content = render_to_string(
        'email/users/account_verification.html',
        {'token': verification_token, 'user': user})
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, "text/html")
    msg.send()


@periodic_task(name='diable_finished_rides', run_every=timedelta(seconds=5))
def disable_finished_rides():
    """Diable finished rides async."""
    now = timezone.now()
    offset = now + timedelta(seconds=5)

    # Update rides that have already finished
    rides = Ride.objects.filter(
        arrival_date__gte=now,
        arrival_date__lte=offset,
        is_active=True)
    rides.update(is_active=False)
"""Utility class and function for 'play' app."""
from typing import Dict, List

from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sessions.models import Session
from django.db.models import Count, Q, QuerySet, Sum
from django.utils import six, timezone


def get_all_logged_in_users() -> QuerySet:
    """Get all logged_in users data."""
    sessions: QuerySet = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list: List = []

    for session in sessions:
        data: Dict = session.get_decoded()
        uid_list.append(data.get("_auth_user_id", None))

    return (
        User.objects.filter(id__in=uid_list)
        .annotate(plays_number=Count("result"))
        .annotate(loses=Count("result", filter=Q(result__count=0)))
        .annotate(draws=Count("result", filter=Q(result__count=-1)))
        .annotate(wins=Count("result", filter=Q(result__count__gt=0)))
        .annotate(points=Sum("result__count"))
    )


def get_all_users_data() -> QuerySet:
    """Get all users data."""
    return (
        User.objects.annotate(plays_number=Count("result"))
        .annotate(loses=Count("result", filter=Q(result__count=0)))
        .annotate(draws=Count("result", filter=Q(result__count=-1)))
        .annotate(wins=Count("result", filter=Q(result__count__gt=0)))
        .annotate(points=Sum("result__count"))
    )


class TokenGenerator(PasswordResetTokenGenerator):
    """Custom token generator class."""

    def _make_hash_value(self, user, timestamp):
        """Rewrite method for email verifying need."""
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()

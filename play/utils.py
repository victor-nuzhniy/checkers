"""Utility class and function for 'play' app."""
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db.models import Count, Q, Sum
from django.utils import timezone


def get_all_logged_in_users():
    """Get all logged_in users data."""
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    return User.objects.filter(
        id__in=uid_list
    ).annotate(
        plays_number=Count('result')
    ).annotate(
        loses=Count('result', filter=Q(result__count=0))
    ).annotate(
        draws=Count('result', filter=Q(result__count=1))
    ).annotate(
        wins=Count('result', filter=Q(result__count=2))
    ).annotate(
        points=Sum('result__count')
    )     # TODO .exclude(is_staff=True)


def get_all_users_data():
    """Get all users data."""
    return User.objects.annotate(
        plays_number=Count('result')
    ).annotate(
        loses=Count('result', filter=Q(result__count=0))
    ).annotate(
        draws=Count('result', filter=Q(result__count=1))
    ).annotate(
        wins=Count('result', filter=Q(result__count=2))
    ).annotate(
        points=Sum('result__count')
    )

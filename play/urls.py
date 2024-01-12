"""Urls list for 'play' app."""
from django.urls import path

from play.views import (
    AccountUpdateView,
    EntryView,
    MainView,
    ProfileView,
    RatingView,
    ResultDeleteView,
    StartView,
)

app_name = 'play'

urlpatterns = [
    path('', EntryView.as_view(), name='entry'),
    path('<int:player_pk>/<int:rival_pk>/', MainView.as_view(), name='main'),
    path('start/', StartView.as_view(), name='start'),
    path('rating/', RatingView.as_view(), name='rating'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('account/update/<int:pk>', AccountUpdateView.as_view(), name='account'),
    path('delete-result/<int:pk>/', ResultDeleteView.as_view(), name='delete_result'),
]

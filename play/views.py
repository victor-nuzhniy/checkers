"""Module for class and function views 'play' app."""
import json
import typing
from abc import ABC

from django import http
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views import generic

from play import forms
from play import play_helpers as helpers
from play.models import Result


class EntryView(generic.TemplateView):
    """Class for entry page."""

    template_name = 'play/entry.html'
    extra_context = {'title': 'Welcome'}


class MainView(UserPassesTestMixin, generic.TemplateView, ABC):
    """Class for main view."""

    template_name = 'play/index.html'
    extra_context = {'title': 'Checkers'}

    def test_func(self, **kwargs: typing.Any) -> bool:
        """Test whether kwargs pk is equal user.zoho_id."""
        if self.request.user.is_anonymous:
            return False
        user_id: int = self.request.user.id
        return user_id in {self.kwargs.get('player_pk'), self.kwargs.get('rival_pk')}

    def get_context_data(self, **kwargs: typing.Any) -> dict:
        """Get context data for the view."""
        if self.request.user.id == self.kwargs.get('player_pk'):
            current_user: int = 1
            receiver: int = self.kwargs.get('rival_pk')
        else:
            current_user = -1
            receiver = self.kwargs.get('player_pk')
        context: dict = super().get_context_data(**kwargs)
        context['player_pk'] = json.dumps(self.kwargs.get('player_pk'))
        context['rival_pk'] = json.dumps(self.kwargs.get('rival_pk'))
        context['current_user'] = current_user
        context['receiver'] = receiver
        return context


class StartView(generic.TemplateView):
    """Class view for start page."""

    template_name = 'play/start.html'
    extra_context = {'title': 'Board'}

    def get_context_data(self, **kwargs: typing.Any) -> dict:
        """Get context data for the view."""
        context: dict = super().get_context_data(**kwargs)
        context['logged_players'] = helpers.get_all_logged_in_users()
        return context


class RatingView(generic.TemplateView):
    """Class view for rating page."""

    template_name = 'play/rating.html'
    extra_context = {'title': 'Rating'}

    def get_context_data(self, **kwargs: typing.Any) -> dict:
        """Get context data for the view."""
        context: dict = super().get_context_data(**kwargs)
        context['players'] = helpers.get_all_users_data().order_by('id')
        context['players_points'] = (
            helpers.get_all_users_data().order_by('points').reverse()
        )
        context['players_plays'] = (
            helpers.get_all_users_data().order_by('plays_number').reverse()
        )
        return context


class ProfileView(UserPassesTestMixin, generic.TemplateView):
    """Class view for user account."""

    template_name = 'play/profile.html'
    extra_context = {'title': 'Player profile'}

    def test_func(self, **kwargs: typing.Any) -> bool:
        """Test whether kwargs pk is equal user.zoho_id."""
        if self.request.user.is_anonymous:
            return False
        return self.request.user.id == self.kwargs.get('pk')

    def get_context_data(self, **kwargs: typing.Any) -> dict:
        """Get context data for the view."""
        context: dict = super().get_context_data(**kwargs)
        statistics: typing.Any | None = (
            helpers.get_all_logged_in_users().filter(id=self.kwargs['pk']).first()
        )
        results_data: QuerySet = Result.objects.filter(
            player=self.kwargs['pk'],
        ).reverse()
        context.update(
            {
                'statistics': statistics,
                'results': results_data,
            },
        )
        return context


class AccountUpdateView(UserPassesTestMixin, generic.FormView, ABC):
    """Class view for change account data."""

    form_class = forms.UserProfileForm
    template_name = 'play/account.html'
    success_url = reverse_lazy('play:start')
    extra_context = {'title': 'Player account'}

    def test_func(self, **kwargs: typing.Any) -> bool:
        """Test whether kwargs pk is equal user.id."""
        if self.request.user.is_anonymous:
            return False
        return self.request.user.id == self.kwargs.get('pk')

    def get_initial(self) -> dict:  # noqa WPS615
        """Return the initial data to use for forms on this view."""
        initial: dict = super().get_initial()
        if self.request.user.is_authenticated:
            initial.update(
                {
                    'username': self.request.user.username,
                    'email': self.request.user.email,
                },
            )
        return initial


class ResultDeleteView(UserPassesTestMixin, generic.FormView, ABC):
    """Class view for deleting result by user."""

    form_class = forms.ResultDeleteForm
    template_name = 'play/profile.html'
    success_url = 'play:profile'

    def test_func(self, **kwargs: typing.Any) -> bool:
        """Test whether kwargs pk is equal user.id."""
        if self.request.user.is_anonymous:
            return False
        return self.request.user.id == self.kwargs.get('pk')

    def get_success_url(self) -> str:  # noqa WPS615
        """Get success url for redirect."""
        url = super().get_success_url()
        return reverse_lazy(url, kwargs={'pk': self.request.user.id})

    def form_valid(self, form: forms.ResultDeleteForm) -> http.HttpResponse:
        """
        Redirect to the success url if the form is valid.

        Perform deleting Result record.
        """
        result_id: typing.Optional[int] = form.cleaned_data.get('id')
        if result_id is not None:
            Result.objects.get(id=result_id).delete()
        return super().form_valid(form)

    def get(
        self,
        request: http.HttpRequest,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> http.HttpResponseRedirect:
        """Rewrite class get method to return get_success_url redirection."""
        url: str = self.get_success_url()
        return http.HttpResponseRedirect(url)

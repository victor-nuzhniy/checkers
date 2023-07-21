"""Module for class and function views 'play' app."""
import json
from abc import ABC
from typing import Any, Dict

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from play.forms import ResultDeleteForm, UserProfileForm
from play.models import Result
from play.utils import get_all_logged_in_users, get_all_users_data


class RegisterView(FormView):
    """Class for User registration."""

    form_class = UserCreationForm
    template_name = "registration/register_form.html"
    extra_context = {"title": "Registration"}
    success_url = reverse_lazy("play:start")

    def form_valid(self, form: UserCreationForm) -> HttpResponseRedirect:
        """Create new user. Add received after creating customer in Zoho CRM zoho_id."""
        user: User = form.save()
        login(self.request, user)
        return super().form_valid(form)


class MainView(UserPassesTestMixin, TemplateView, ABC):
    """Class for main view."""

    template_name = "play/index.html"
    extra_context = {"title": "Checkers"}

    def test_func(self, **kwargs: Any) -> bool:
        """Test whether kwargs pk is equal user.zoho_id."""
        if self.request.user.is_anonymous:
            return False
        user_id: int = self.request.user.id
        return user_id in {self.kwargs.get("player_pk"), self.kwargs.get("rival_pk")}

    def get_context_data(self, **kwargs: Any) -> Dict:
        """Get context data for the view."""
        if self.request.user.id == self.kwargs.get("player_pk"):
            current_user: int = 1
            receiver: int = self.kwargs.get("rival_pk")
        else:
            current_user = -1
            receiver = self.kwargs.get("player_pk")
        context: Dict = super().get_context_data(**kwargs)
        context["player_pk"] = json.dumps(self.kwargs.get("player_pk"))
        context["rival_pk"] = json.dumps(self.kwargs.get("rival_pk"))
        context["current_user"] = current_user
        context["receiver"] = receiver
        return context


class StartView(TemplateView):
    """Class view for start page."""

    template_name = "play/start.html"
    extra_context = {"title": "Board"}

    def get_context_data(self, **kwargs: Any) -> Dict:
        """Get context data for the view."""
        context: Dict = super().get_context_data(**kwargs)
        context["logged_players"] = get_all_logged_in_users()
        return context


class RatingView(TemplateView):
    """Class view for rating page."""

    template_name = "play/rating.html"
    extra_context = {"title": "Rating"}

    def get_context_data(self, **kwargs: Any) -> Dict:
        """Get context data for the view."""
        context: Dict = super().get_context_data(**kwargs)
        context["players"] = get_all_users_data()
        context["players_points"] = get_all_users_data().order_by("points")
        context["players_plays"] = get_all_users_data().order_by("plays_number")
        return context


class ProfileView(UserPassesTestMixin, TemplateView):
    """Class view for user account."""

    template_name = "play/profile.html"
    extra_context = {"title": "Player profile"}

    def test_func(self, **kwargs: Any) -> bool:
        """Test whether kwargs pk is equal user.zoho_id."""
        if self.request.user.is_anonymous:
            return False
        return self.request.user.id == self.kwargs.get("pk")

    def get_context_data(self, **kwargs: Any) -> Dict:
        """Get context data for the view."""
        context: Dict = super().get_context_data(**kwargs)
        statistics: QuerySet = get_all_logged_in_users().filter(
            id=self.kwargs["pk"]
        ).first()
        results: QuerySet = Result.objects.filter(player=self.kwargs["pk"]).reverse()
        context.update(
            {
                "statistics": statistics,
                "results": results,
            }
        )
        return context


class AccountUpdateView(UserPassesTestMixin, FormView, ABC):
    """Class view for change account data."""

    form_class = UserProfileForm
    template_name = "play/account.html"
    success_url = reverse_lazy("play:start")
    extra_context = {"title": "Player account"}

    def test_func(self, **kwargs: Any) -> bool:
        """Test whether kwargs pk is equal user.id."""
        if self.request.user.is_anonymous:
            return False
        return self.request.user.id == self.kwargs.get("pk")

    def get_initial(self) -> Dict:
        """Return the initial data to use for forms on this view."""
        initial: Dict = super().get_initial()
        initial.update(
            {"username": self.request.user.username, "email": self.request.user.email}
        )
        return initial


class ResultDeleteView(UserPassesTestMixin, FormView, ABC):
    """Class view for deleting result by user."""

    form_class = ResultDeleteForm
    template_name = "play/profile.html"
    success_url = "play:profile"

    def test_func(self, **kwargs: Any) -> bool:
        """Test whether kwargs pk is equal user.id."""
        if self.request.user.is_anonymous:
            return False
        return self.request.user.id == self.kwargs.get("pk")

    def get_success_url(self) -> HttpResponseRedirect:
        """Get success url for redirect."""
        url = super().get_success_url()
        return reverse_lazy(url, kwargs={"pk": self.request.user.id})

    def form_valid(self, form: ResultDeleteForm) -> HttpResponseRedirect:
        """
        Redirect to the success url if the form is valid.

        Perform deleting Result record.
        """
        Result.objects.get(id=form.cleaned_data.get("id")).delete()
        return super().form_valid(form)

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseRedirect:
        """Rewrite class get method to return get_success_url redirection."""
        return HttpResponseRedirect(self.get_success_url())

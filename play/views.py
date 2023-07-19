"""Module for class and function views 'play' app."""
import json
from abc import ABC
from typing import Dict, Any

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from play.forms import UserProfileForm
from play.models import Result
from play.utils import get_all_logged_in_users


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
        return super().form_valid(
            form
        )


class MainView(TemplateView):
    """Class for main view."""

    template_name = "play/index.html"

    def get_context_data(self, **kwargs: Any) -> Dict:
        """Get context data for the view."""
        if self.request.user.id == self.kwargs.get("player_pk"):
            current_user = 1
            receiver = self.kwargs.get("rival_pk")
        else:
            current_user = -1
            receiver = self.kwargs.get("player_pk")
        context = super().get_context_data(**kwargs)
        context["player_pk"] = json.dumps(self.kwargs.get("player_pk"))
        context["rival_pk"] = json.dumps(self.kwargs.get("rival_pk"))
        context["current_user"] = current_user
        context["receiver"] = receiver
        return context


class StartView(TemplateView):
    """Class view for start page."""

    template_name = 'play/start.html'

    def get_context_data(self, **kwargs: Any) -> Dict:
        """Get context data for the view."""
        context = super().get_context_data(**kwargs)
        context["logged_players"] = get_all_logged_in_users()
        return context


class ProfileView(UserPassesTestMixin, TemplateView):
    """Class view for user account."""

    template_name = "play/profile.html"

    def test_func(self, **kwargs: Any) -> bool:
        """Test whether kwargs pk is equal user.zoho_id."""
        if self.request.user.is_anonymous:
            return False
        return self.request.user.id == self.kwargs.get("pk")

    def get_context_data(self, **kwargs: Any) -> Dict:
        """Get context data for the view."""
        context = super().get_context_data(**kwargs)
        statistics = get_all_logged_in_users().filter(id=self.kwargs["pk"]).first()
        results = Result.objects.filter(player=self.kwargs["pk"]).reverse()
        context.update({
            "statistics": statistics,
            "results": results,
        })
        return context


class AccountUpdateView(UserPassesTestMixin, FormView, ABC):
    """Class view for change account data."""

    form_class = UserProfileForm
    template_name = "play/account.html"
    success_url = reverse_lazy("play:start")

    def test_func(self, **kwargs: Any) -> bool:
        """Test whether kwargs pk is equal user.zoho_id."""
        if self.request.user.is_anonymous:
            return False
        return self.request.user.id == self.kwargs.get("pk")

    def get_initial(self) -> Dict:
        """Return the initial data to use for forms on this view."""
        initial: Dict = super().get_initial()
        initial.update({
            "username": self.request.user.username, "email": self.request.user.email
        })
        return initial

    def get_context_data(self, **kwargs: Any) -> Dict:
        """Get context data for the view."""
        context = super().get_context_data(**kwargs)

        return context



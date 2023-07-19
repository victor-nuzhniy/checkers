"""Module for class and function views 'play' app."""
import json
from typing import Dict

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from play.utils import get_all_logged_in_users


class RegisterView(FormView):
    """Class for User registration."""

    form_class = UserCreationForm
    template_name = "registration/register_form.html"
    extra_context = {"title": "Registration"}
    success_url = reverse_lazy("play:registration")

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

    def get_context_data(self, **kwargs) -> Dict:
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
    """Class for start page view."""

    template_name = 'play/start.html'

    def get_context_data(self, **kwargs) -> Dict:
        """Get context data for the view."""
        context = super().get_context_data(**kwargs)
        context["logged_players"] = get_all_logged_in_users()
        return context

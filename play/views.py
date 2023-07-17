"""Module for class and function views 'play' app."""
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView


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

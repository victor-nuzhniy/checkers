"""Module for class and function views 'play' app."""
import json
from abc import ABC
from typing import Any, Dict, Optional

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import FormView, TemplateView

from play.forms import ResultDeleteForm, SignupForm, UserProfileForm
from play.models import Result
from play.utils import (
    account_activation_token,
    get_all_logged_in_users,
    get_all_users_data,
)


class RegisterView(FormView):
    """Class for User registration."""

    form_class = SignupForm
    template_name = "play/registration/register_form.html"
    extra_context = {"title": "Registration"}
    success_url = reverse_lazy("play:email_confirm")

    def form_valid(self, form: SignupForm) -> HttpResponseRedirect:
        """Create new user. Add received after creating customer in Zoho CRM zoho_id."""
        user: User = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject: str = "Activate your account"
        message: str = render_to_string(
            "play/registration/email_template.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            },
        )
        to_email: str = form.cleaned_data.get("email")
        send_mail(mail_subject, message, "admin@email.com", [to_email])
        return super().form_valid(form)


class RegisterEmailConfirmView(TemplateView):
    """Class view for redirection after registration."""

    template_name = "play/registration/email_confirm.html"
    extra_context = {"title": "Email confirmation"}


class EmailActivationView(TemplateView):
    """Class view for getting activation info."""

    template_name = "play/registration/email_activation_result.html"
    extra_context = {"title": "Email activation"}

    def get_context_data(self, **kwargs: Any) -> Dict:
        """Get context data for the view."""
        context = super().get_context_data(**kwargs)
        try:
            uid = force_str(urlsafe_base64_decode(self.kwargs.get("uidb64")))
            user: Optional[User] = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(
            user, self.kwargs.get("token")
        ):
            user.is_active = True
            user.save()
            message = (
                "Thank you for your email confirmation. Now you can login your account."
            )
        else:
            message = "Activation link is not valid!"
        context["message"] = message
        return context


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
        context["players"] = get_all_users_data().order_by("id")
        context["players_points"] = get_all_users_data().order_by("points").reverse()
        context["players_plays"] = (
            get_all_users_data().order_by("plays_number").reverse()
        )
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
        statistics: QuerySet = (
            get_all_logged_in_users().filter(id=self.kwargs["pk"]).first()
        )
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

"""Admin site configuration for 'play' app."""
from django.contrib import admin
from django.contrib.sessions.models import Session

from play.models import Result


class ResultAdmin(admin.ModelAdmin):
    """Result admin site settings."""

    list_display = ("id", "player", "rival", "count")
    list_display_links = ("id", "player")


class SessionAdmin(admin.ModelAdmin):
    """Session admin site settings."""

    @staticmethod
    def _session_data(obj):
        """Return decoded data."""
        return obj.get_decoded()

    list_display = ["session_key", "_session_data", "expire_date"]
    list_display_links = ["session_key"]


admin.site.register(Result, ResultAdmin)
admin.site.register(Session, SessionAdmin)

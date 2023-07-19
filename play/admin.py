"""Admin site configuration for 'play' app."""
from django.contrib import admin

from play.models import Result


class ResultAdmin(admin.ModelAdmin):
    """Result admin site settings."""

    list_display = ("id", "player", "rival", "count")
    list_display_links = ("id", "player")


admin.site.register(Result, ResultAdmin)

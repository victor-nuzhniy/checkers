"""Admin site configuration for 'play' app."""
from django.contrib import admin
from django.contrib.sessions.models import Session

from play.models import ResultData


class ResultAdminData(admin.ModelAdmin):
    """Result admin site settings."""

    list_display = ('id', 'player', 'rival', 'count')
    list_display_links = ('id', 'player')


class SessionAdmin(admin.ModelAdmin):
    """Session admin site settings."""

    def _session_data(self, session_object: Session) -> dict:
        """Return decoded data."""
        return session_object.get_decoded()

    list_display = ['session_key', '_session_data', 'expire_date']
    list_display_links = ['session_key']


admin.site.register(ResultData, ResultAdminData)
admin.site.register(Session, SessionAdmin)

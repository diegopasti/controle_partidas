from django.contrib import admin
from apps.game.admin.base import ResultAdmin
from apps.game.models import Booking


@admin.register(Booking)
class BookingAdmin(ResultAdmin):

    actions_on_bottom = True
    actions_on_top = False

    list_display = (
        "company", "area", "group", "owner", "date", "hour", "status", "best_player", "total_players",
        "total_teams", "total_matches", "total_gols", "start", "finish", "duration",
    )

    fieldsets = (
        ("Reserva", {
            "fields": (
                "company", "area", "group", "owner", "status", "date", "hour",
            )
        }),

        ("Resultado", {
            "fields": (
                "best_player", "total_players", "total_teams", "total_matches", "total_gols",
                "start", "finish", "duration",)
        }),
    )

    add_fieldsets = (
        ("Reserva", {
            "fields": ("company", "area", "group", "owner", "players", "date", "hour")
        }),
    )

    readonly_fields = ["creation_date", "created_by", "last_update", "updated_by"]

    def get_fieldsets(self, request, obj=None):
        if not obj:
             return self.add_fieldsets
        return super(BookingAdmin, self).get_fieldsets(request, obj)


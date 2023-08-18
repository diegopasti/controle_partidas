from django.contrib import admin
from apps.game.admin.base import ResultAdmin
from apps.game.models import Match


@admin.register(Match)
class MatchAdmin(ResultAdmin):

    actions_on_bottom = True
    actions_on_top = False

    list_display = (
        "booking", "start", "finish", "duration",
        "first_team", "second_team", "gols", "first_team_gols", "second_team_gols"
    )

    fieldsets = (
        ("Partida", {
            "fields": ("booking", "first_team", "second_team", "first_team_gols", "second_team_gols",)
        }),

        ("Resultado", {
            "fields": ("start", "finish", "duration",)
        }),
    )

    add_fieldsets = (
        ("Partida", {
            "fields": ("booking", "first_team", "second_team", "start",)
        }),
    )

    readonly_fields = ["creation_date", "created_by", "last_update", "updated_by"]

    def get_fieldsets(self, request, obj=None):
        if not obj:
             return self.add_fieldsets
        return super(MatchAdmin, self).get_fieldsets(request, obj)

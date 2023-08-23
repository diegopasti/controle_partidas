from django.contrib import admin
from apps.game.admin.base import ResultAdmin
from apps.game.models import Team


@admin.register(Team)
class TeamAdmin(ResultAdmin):

    actions_on_bottom = True
    actions_on_top = False

    list_filter = [
        "players",
        "created_by"
    ]

    list_display = (
        #"booking",
        "code", "name", "best_player", "gols", #"total_rounds", "total_round_duration",
        #"total_round_average", "column_separator", "created", "updated"
    )

    fieldsets = (
        ("Jogadores", {
         "fields": ("booking", "name", "players",)
        }),

        ("Resultados", {
            "fields": ("total_rounds", "total_round_duration", "total_round_average",)
        }),

        ("Alterações", {
         "fields": ("created_by", "creation_date", "updated_by", "last_update", "is_active")
        }),
    )

    add_fieldsets = (
        ("Geral", {
            "fields": ("booking", "name", "players",)
        }),
    )

    readonly_fields = ["creation_date", "created_by", "last_update", "updated_by"]

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(TeamAdmin, self).get_fieldsets(request, obj)



    def best_player(self, obj):
        return self.double_row(f"{obj.best_player}", f"")

    def total_time(self, obj):
        return self.double_row(f"{obj.total_round_duration}", f"Em {obj.total_rounds} rodadas")

    best_player.allow_tags = True
    best_player.short_description = "Melhor do Time"
    best_player.admin_order_field = "best_player"

    total_time.allow_tags = True
    total_time.short_description = "Tempo Jogado"
    total_time.admin_order_field = 'total_round_duration'

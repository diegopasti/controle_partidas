from django.contrib import admin
from faker import Faker

from apps.game.admin.base import ResultAdmin
from apps.game.forms import CreationPlayerForm
from apps.game.models import Player


@admin.register(Player)
class PlayerAdmin(ResultAdmin):

    actions_on_bottom = True
    actions_on_top = False
    search_fields = ['name']
    list_filter = ["best_of_match", "best_of_team", "created_by", "updated_by"]
    add_form = CreationPlayerForm

    list_display = (
        "name", "column_separator",
        "best_per_team", "best_per_match", "column_separator",
        "gols_per_match", "victories_result", "losses_result", "empaths_result", "column_separator",
        "created", "updated"
    )

    add_fieldsets = (
        ("Jogador", {
            "fields": ("name", )
        }),
    )

    fieldsets = (
        ("Jogador", {
            "fields": ("name", "total_matches", "total_gols", "gols_rate", "best_of_team", "best_of_match",)
        }),

        ("Partidas", {
            "fields": ("matches",)
        }),

        ("Alterações", {
            "fields": ("user", "created_by", "creation_date", "updated_by", "last_update", "is_active")
        }),
    )

    readonly_fields = ["creation_date", "created_by", "last_update", "updated_by"]

    @admin.action(description="Importar jogadores")
    def import_players(modeladmin, request, queryset):
        fake = Faker()
        for person in range(50):
            player = Player()
            player.name = fake.unique.first_name_male().upper() + " " + fake.last_name_male().upper()
            player.created_by = request.user
            player.updated_by = request.user
            player.save()

    def get_fieldsets(self, request, obj=None, **kwargs):
        """
        Use special form during foo creation
        """

        if obj is None:
            return self.add_fieldsets

        return self.fieldsets

    def gols_per_match(self, obj):
        return self.double_row(f"{obj.total_gols}", f"{obj.gols_rate} POR PARTIDA")

    def best_per_match(self, obj):
        return self.double_row(f"{obj.best_of_match} vezes", f"EM {obj.total_matches} PARTIDAS")

    def best_per_team(self, obj):
        return self.double_row(f"{obj.best_of_team} vezes", f"EM {obj.total_matches} PARTIDAS")

    gols_per_match.allow_tags = True
    gols_per_match.short_description = "Gols"
    gols_per_match.admin_order_field = 'gols'

    best_per_match.allow_tags = True
    best_per_match.short_description = "Melhor da Partida"
    best_per_match.admin_order_field = 'best_of_match'

    best_per_team.allow_tags = True
    best_per_team.short_description = "Melhor do Time"
    best_per_team.admin_order_field = 'best_of_team'

    actions = [import_players]

    #form = SpecialityAdminForm
    #list_display = ("name", "question_count", "main_speciality", "all_tags",)
    #list_filter = ("main_speciality",)
    #ordering = ("name",)
    #search_fields = ("name",)

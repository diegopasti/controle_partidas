from django.contrib import admin
from django.db import models
from django.forms import TextInput, Select, SelectMultiple

from apps.core.admin import BaseModelAdmin, StatusFilter
from apps.game.forms import CreationPlayerForm
from apps.game.models import Player


@admin.register(Player)
class PlayerAdmin(BaseModelAdmin):

    actions_on_bottom = True
    actions_on_top = False
    search_fields = ['name']
    list_filter = [
        "gols",
        "best_of_match",
        "best_of_team",
        #("created_by", StatusFilter),
        "created_by",
        "updated_by",
    ]

    add_form = CreationPlayerForm

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={"style": "min-width:100vh"})},
        models.IntegerField: {'widget': TextInput(attrs={"style": "min-width:100vh"})},
        models.DecimalField: {'widget': TextInput(attrs={"style": "width:100%"})},
        models.DateTimeField: {'widget': TextInput(attrs={"style": "width:100%"})},
        models.DateField: {'widget': TextInput(attrs={"style": "width:100%"})},
        models.DurationField: {'widget': TextInput(attrs={"style": "width:100%"})},
        models.ForeignKey: {'widget': Select(attrs={"style": "min-width:100vh"})},
        models.ManyToManyField: {'widget': SelectMultiple(attrs={"style": "min-width:100vh"})},
    }

    list_display = (
        "name", "column_separator",
        "best_per_team", "best_per_match", "column_separator",
        "gols_per_match", "victories_result", "losses_result", "empaths_result", "column_separator",
        "created", "updated"
    )

    fieldsets = (
        ("Jogador", {
            "fields": ("name", "total_matchs", "total_rounds", "gols", "gols_rate", "best_of_team", "best_of_match",)
        }),

        ("Partidas", {
            "fields": ("matchs",)
        }),

        ("Rodadas", {
            "fields": ("rounds",)
        }),

        ("Alterações", {
            "fields": ("created_by", "creation_date", "updated_by", "last_update", "is_active")
        }),
    )

    readonly_fields = ["creation_date", "created_by", "last_update", "updated_by"]

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during foo creation
        """
        defaults = {}
        if obj is None:
            defaults["form"] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def gols_per_match(self, obj):
        return self.double_row(f"{obj.gols}", f"{obj.gols_rate} POR PARTIDA")

    def victories_result(self, obj):
        return self.double_row(f"{obj.victories}", f"{obj.victories_rate}%")

    def losses_result(self, obj):
        return self.double_row(f"{obj.losses}", f"{obj.losses_rate}%")

    def empaths_result(self, obj):
        return self.double_row(f"{obj.empaths}", f"{obj.empaths_rate}%")

    def best_per_match(self, obj):
        return self.double_row(f"{obj.best_of_match} vezes", f"EM {obj.total_matchs} PARTIDAS")

    def best_per_team(self, obj):
        return self.double_row(f"{obj.best_of_team} vezes", f"EM {obj.total_matchs} PARTIDAS")

    def created(self, obj):
        return self.double_row(
            f"{obj.creation_date.strftime('%d/%m/%Y às %H:%M:%S')}", f"POR {obj.created_by.username.upper()}"
        )

    def updated(self, obj):
        return self.double_row(
            f"{obj.last_update.strftime('%d/%m/%Y às %H:%M:%S')}", f"POR {obj.updated_by.username.upper()}"
        )

    gols_per_match.allow_tags = True
    gols_per_match.short_description = "Gols"
    gols_per_match.admin_order_field = 'gols'

    victories_result.allow_tags = True
    victories_result.short_description = "Vitórias"
    victories_result.admin_order_field = 'victories'

    empaths_result.allow_tags = True
    empaths_result.short_description = "Empates"
    empaths_result.admin_order_field = 'empaths'

    losses_result.allow_tags = True
    losses_result.short_description = "Derrotas"
    losses_result.admin_order_field = 'losses'

    best_per_match.allow_tags = True
    best_per_match.short_description = "Melhor da Partida"
    best_per_match.admin_order_field = 'best_of_match'

    best_per_team.allow_tags = True
    best_per_team.short_description = "Melhor do Time"
    best_per_team.admin_order_field = 'best_of_team'

    created.allow_tags = True
    created.short_description = "Cadastrado em"
    created.admin_order_field = 'creation_date'

    updated.allow_tags = True
    updated.short_description = "Atualizado em"
    updated.admin_order_field = 'last_updated'

    #form = SpecialityAdminForm
    #list_display = ("name", "question_count", "main_speciality", "all_tags",)
    #list_filter = ("main_speciality",)
    #ordering = ("name",)
    #search_fields = ("name",)
from django.contrib import admin
from django.db import models
from django.forms import TextInput, Select, SelectMultiple
from django.utils.html import format_html

from apps.core.admin import BaseModelAdmin
from apps.game.forms import CreationPlayerForm
from apps.game.models import Player


@admin.register(Player)
class PlayerAdmin(BaseModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={"style": "min-width:100vh"})},
        models.IntegerField: {'widget': TextInput(attrs={"style": "min-width:100vh"})},
        models.DecimalField: {'widget': TextInput(attrs={"style": "width:100%"})},
        models.DateTimeField: {'widget': TextInput(attrs={"style": "width:100%"})},
        models.DateField: {'widget': TextInput(attrs={"style": "width:100%"})},
        models.DurationField: {'widget': TextInput(attrs={"style": "width:100%"})},
        models.ForeignKey: {'widget': Select(attrs={"style": "min-width:100vh"})},
        models.ManyToManyField: {'widget': SelectMultiple(attrs={"style": "min-width:100vh"})},

        #models.BooleanField: {'widget': CheckboxInput(attrs={"style": "float:right;'"})},
        #models.ForeignKey: {'widget': Select(attrs={'size': '100'})},
        #models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

    add_form = CreationPlayerForm

    list_display = (
        "name",
        "best_per_team", "best_per_match",  # "matchs", "rounds",
        "gols_per_match", "victories_result", "losses_result", "empaths_result",
        "created", "updated"
    )

    # fields = (
    #     "name",
    #     "victories", "victories_rate", "empaths", "empaths_rate", "losses", "losses_rate",
    #
    #     "best_of_team", "best_of_match", "total_matchs", "total_rounds", "gols", "gols_rate", "matchs", "rounds",
    #     "created_by", "creation_date", "updated_by", "last_update", "is_active",
    # )

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
        return self.double_row(f"{obj.gols}", f"{obj.gols_rate} por partida")

    def victories_result(self, obj):
        return self.double_row(f"{obj.victories}", f"{obj.victories_rate}%")

    def losses_result(self, obj):
        return self.double_row(f"{obj.losses}", f"{obj.losses_rate}%")

    def empaths_result(self, obj):
        return self.double_row(f"{obj.empaths}", f"{obj.empaths_rate}%")

    def best_per_match(self, obj):
        return self.double_row(f"{obj.best_of_match} vezes", f"em {obj.total_matchs} Partidas")

    def best_per_team(self, obj):
        return self.double_row(f"{obj.best_of_team} vezes", f"em {obj.total_matchs} Partidas")

    def created(self, obj):
        return self.double_row(
            f"{obj.creation_date.strftime('%d/%m/%Y às %H:%M:%S')}", f"por {obj.created_by}"
        )

    def updated(self, obj):
        return self.double_row(
            f"{obj.last_update.strftime('%d/%m/%Y às %H:%M:%S')}", f"por {obj.updated_by}"
        )

    def double_row(self, first_value, second_value):
        message = format_html(
            f"<div style='text-align:center;white-space: nowrap;'>{first_value}<br><sub style='color:#777;'>{second_value}</sub></div>")
        return message

    gols_per_match.allow_tags = True
    gols_per_match.short_description = "Gols"

    victories_result.allow_tags = True
    victories_result.short_description = "Vitórias"

    empaths_result.allow_tags = True
    empaths_result.short_description = "Empates"

    losses_result.allow_tags = True
    losses_result.short_description = "Derrotas"

    best_per_match.allow_tags = True
    best_per_match.short_description = "Melhor da Partida"

    best_per_team.allow_tags = True
    best_per_team.short_description = "Melhor do Time"

    created.allow_tags = True
    created.short_description = "Cadastrado em"

    updated.allow_tags = True
    updated.short_description = "Atualizado em"



    #form = SpecialityAdminForm
    #list_display = ("name", "question_count", "main_speciality", "all_tags",)
    #list_filter = ("main_speciality",)
    #ordering = ("name",)
    #search_fields = ("name",)
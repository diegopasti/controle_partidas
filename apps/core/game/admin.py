from django.contrib import admin
from django.utils.html import format_html

from apps.core.game.models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):

    fields = (
        'name',
    )

    list_display = (
        'name',
        'best_per_team', 'best_per_match',  #'matchs', 'rounds',
        'gols_per_match', 'victories_result', 'losses_result', 'empaths_result',
        'creation_date', 'last_update', 'is_active' # 'created_by', 'updated_by', 'creation_date', 'last_update', 'is_active'
    )

    def gols_per_match(self, obj):
        return self.double_row(obj.gols_rate, obj.gols)

    def victories_result(self, obj):
        return self.double_row(obj.victories_rate, obj.victories)

    def losses_result(self, obj):
        return self.double_row(obj.losses_rate, obj.losses)

    def empaths_result(self, obj):
        return self.double_row(obj.empaths_rate, obj.empaths)

    def best_per_match(self, obj):
        return self.double_row(f"{obj.best_of_match} vezes", f"em {obj.total_matchs} Partidas")

    def best_per_team(self, obj):
        return self.double_row(f"{obj.best_of_team} vezes", f"em {obj.total_matchs} Partidas")

    def double_row(self, first_value, second_value):
        message = format_html(
            f"<div style='text-align:left;white-space: nowrap;'>{first_value}<br><sub style='color:#777;'>{second_value}</sub></div>")
        return message

    gols_per_match.allow_tags = True
    gols_per_match.short_description = 'Gols'

    victories_result.allow_tags = True
    victories_result.short_description = 'Vitórias'

    empaths_result.allow_tags = True
    empaths_result.short_description = 'Empates'

    losses_result.allow_tags = True
    losses_result.short_description = 'Derrotas'

    best_per_match.allow_tags = True
    best_per_match.short_description = 'Melhor da Partida'

    best_per_team.allow_tags = True
    best_per_team.short_description = 'Melhor do Time'



    #form = SpecialityAdminForm
    #list_display = ('name', 'question_count', 'main_speciality', 'all_tags',)
    #list_filter = ('main_speciality',)
    #ordering = ('name',)
    #search_fields = ('name',)
import random
from math import ceil

from django.contrib import admin
from apps.game.admin.base import ResultAdmin
from apps.game.models import Booking, Team


@admin.register(Booking)
class BookingAdmin(ResultAdmin):

    actions_on_bottom = True
    actions_on_top = False

    search_fields = ['group__name']

    list_display = (
        "local", "player_group", "time", "status", "column_separator", "matches", "teams",
        "best_player", "start", "finish", "duration",
    )

    fieldsets = (
        ("Reserva", {
            "fields": (
                "company", "area", "group", "owner", "status", "date", "hour",
            )
        }),

        ("Jogadores", {
            "fields": ("players", "goalkeepers", "goalkeepers_fixed")
        }),

        ("Resultado", {
            "fields": (
                "best_player", "total_players", "total_teams", "total_matches", "total_gols",
                "start", "finish", "duration",)
        }),
    )

    add_fieldsets = (
        ("Local e Horário", {
            "fields": ("date", "hour", "company", "area")
        }),

        ("Jogadores", {
            "fields": ("owner", "group", "players", "goalkeepers", "goalkeepers_fixed")
        }),
    )

    readonly_fields = ["creation_date", "created_by", "last_update", "updated_by"]

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(BookingAdmin, self).get_fieldsets(request, obj)

    @admin.action(description="Sortear Times")
    def sort_teams(self, request, queryset):
        for booking in queryset:
            #if booking.total_teams > 0:
            #    print("Reserva já tem times definidos")
            #    return False

            max_players = booking.area.players
            total_goalkeepers = booking.goalkeepers.count()
            sortable_players = booking.players

            goalkeepers_fixed = booking.goalkeepers_fixed and total_goalkeepers == 2
            if goalkeepers_fixed:
                print("GOLEIROS FIXOS, ENTAO SO SORTEA NA LISTA DE JOGADORES")
                max_players -= 2
            else:
                print("SEM GOLEIROS FIXOS, ENTAO SORTEIA TODOS JOGADORES")
                sortable_players += booking.goalkeepers

            print("VOU SORTEAR:", sortable_players.all(), sortable_players.count())
            print("VOU SORTEAR:", sortable_players.count() / max_players)

            booking.total_players = booking.players.count() + total_goalkeepers
            booking.total_teams = ceil(sortable_players.count()/max_players)


            #booking.save()
            players = random.sample(list(sortable_players.all()), sortable_players.count())
            print("PLAYERS:",players)

            #if booking.total_players % booking.area.players:

            for item in range(booking.total_teams):
                team = Team()
                #team.booking = booking
                team.code = item+1
                team.name = f"Time{item+1}"
                initial_position = item*max_players
                end_position = (item+1)*max_players

                #team.save()
                #team.players.set(players[initial_position:end_position])
                #team.save()
                print("TIME:", team)

    def player_group(self, obj):
        return self.double_row(
            f"{obj.group.name.upper()}",
            f"ORGANIZADOR: {obj.owner.get_full_name().upper()}",
            align="left"
        )

    def time(self, obj):
        return self.double_row(
            f"{obj.hour}",
            f"{obj.date}",
            align="center"
        )

    def local(self, obj):
        return self.double_row(
            f"{obj.company.name.upper()}",
            f"{obj.area.type.upper()} - {obj.area.name.upper()}",
            align="left"
        )

    def teams(self, obj):
        return self.double_row(
            f"{obj.total_players}",
            f"EM {obj.total_teams} TIMES",
            align="center"
        )

    def matches(self, obj):
        return self.double_row(
            f"{obj.total_gols}",
            f"EM {obj.total_matches} PARTIDAS",
            align="center"
        )

    actions = [sort_teams]

    local.allow_tags = True
    local.short_description = "Local"
    local.admin_order_field = "company"

    time.allow_tags = True
    time.short_description = "Horário"
    time.admin_order_field = "date"

    player_group.allow_tags = True
    player_group.short_description = "Grupo"
    player_group.admin_order_field = "group"

    teams.allow_tags = True
    teams.short_description = "Jogadores"
    teams.admin_order_field = "team"

    matches.allow_tags = True
    matches.short_description = "Partidas"
    matches.admin_order_field = "total_matches"

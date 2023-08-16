from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import gettext_lazy as _

from apps.core.models import BaseModel


class ResultFields(models.Model):

    class Meta:
        abstract = True

    victories = models.IntegerField("Total de Vitórias", default=0, blank=True)
    losses = models.IntegerField("Total de Gols", default=0, blank=True)
    empaths = models.IntegerField("Total de Empates", default=0, blank=True)

    victories_rate = models.DecimalField(
        "Percentual de Vitórias", max_digits=10, decimal_places=2, blank=True, default=0
    )

    losses_rate = models.DecimalField(
        "Percentual de Derrotas", max_digits=10, decimal_places=2, blank=True, default=0
    )

    empaths_rate = models.DecimalField(
        "Percentual de Empates", max_digits=10, decimal_places=2, blank=True, default=0
    )


class Player(BaseModel, ResultFields):
    class Meta:
        db_table = "apps_game_player"
        verbose_name = "Jogador"
        verbose_name_plural = "Jogadores"

    name = models.CharField(_('Nome'), max_length=50, unique=True, blank=False)
    total_matchs = models.IntegerField("Total de Partidas", default=0, blank=True)
    total_rounds = models.IntegerField("Total de Rodadas", default=0, blank=True)
    gols = models.IntegerField("Total de Gols", default=0, blank=True)
    gols_rate = models.IntegerField("Gols por Partidas", default=0, blank=True)

    best_of_team = models.IntegerField(
        "Melhor do time", default=0, blank=True,
        help_text="Número de vezes em que foi o melhor do time em uma partida")

    best_of_match = models.IntegerField(
        "Melhor da partida", default=0, blank=True,
        help_text="Número de vezes em que foi o melhor da partida"
    )

    matchs = models.ManyToManyField('Match', verbose_name=_("Partidas"), blank=True)
    rounds = models.ManyToManyField('Round', verbose_name=_("Rodadas"), blank=True)

    def __str__(self):
        return self.name


class Match(models.Model):
    class Meta:
        db_table = "apps_game_match"
        verbose_name = "Jogador"
        verbose_name_plural = "Jogadores"

    start = models.DateTimeField()
    finish = models.DateTimeField()
    duration = models.DurationField()

    players = models.ManyToManyField(Player)
    best_player = models.ForeignKey(
        Player, related_name="%(app_label)s_%(class)s_best_player", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    total_players = models.IntegerField("Total de Jogadores", default=0, blank=True)
    total_teams = models.IntegerField("Total de Times", default=0, blank=True)

    total_rounds = models.IntegerField("Total de Partidas", default=0, blank=True)

    gols = models.IntegerField("Total de Gols", default=0, blank=True)
    victories = models.IntegerField("Total de Vitórias", default=0, blank=True)
    losses = models.IntegerField("Total de Gols", default=0, blank=True)
    empaths = models.IntegerField("Total de Empates", default=0, blank=True)

    created_by = models.ForeignKey(
        User, related_name="%(app_label)s_%(class)s_created_by", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    updated_by = models.ForeignKey(
        User, related_name="%(app_label)s_%(class)s_updated_by", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    creation_date = models.DateTimeField(_('Data de criação'), null=True, auto_now_add=True)
    last_update = models.DateTimeField(_('Última atualização'), null=True, auto_now=True)
    is_active = models.BooleanField(_('Ativo'), null=False, default=True)


class Team(BaseModel, ResultFields):
    class Meta:
        db_table = "apps_game_team"
        verbose_name = "Time"
        verbose_name_plural = "Times"

    match = models.ForeignKey(
        Match, related_name="%(app_label)s_%(class)s_match", verbose_name="Partida",
        null=True, blank=True, on_delete=models.DO_NOTHING
    )

    code = models.IntegerField("Codigo", default=1, null=True, blank=True)

    name = models.CharField(_('Nome do Time'), max_length=50, blank=False)

    players = models.ManyToManyField(Player, verbose_name="Jogadores")

    best_player = models.ForeignKey(
        Player, related_name="%(app_label)s_%(class)s_best_player", verbose_name="Melhor jogador do Time",
        null=True, blank=True, on_delete=models.DO_NOTHING
    )

    gols = models.IntegerField("Total de Gols", default=0, blank=True)
    total_rounds = models.IntegerField("Total de Rodadas", default=0, blank=True)
    total_round_duration = models.DurationField(
        "Tempo total em jogo", default=timedelta(seconds=0), null=True, blank=True
    )
    total_round_average = models.DurationField(
        "Tempo médio por rodada", default=timedelta(seconds=0), null=True, blank=True
    )


class Round(models.Model):

    class Meta:
        db_table = "apps_game_round"
        verbose_name = "Rodada"
        verbose_name_plural = "Rodada"

    start = models.DateTimeField()
    finish = models.DateTimeField()
    duration = models.DurationField()

    first_team = models.ForeignKey(
        Team, related_name="%(app_label)s_%(class)s_first_team", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    second_team = models.ForeignKey(
        Team, related_name="%(app_label)s_%(class)s_second_team", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    players = models.ManyToManyField(Player)
    total_players = models.IntegerField("Total de Jogadores", default=0, blank=True)

    best_player = models.ForeignKey(
        Player, related_name="%(app_label)s_%(class)s_best_player", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    match = models.ForeignKey(
        Player, related_name="%(app_label)s_%(class)s_match", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    gols = models.IntegerField("Total de Gols", default=0, blank=True)
    victories = models.IntegerField("Total de Vitórias", default=0, blank=True)
    losses = models.IntegerField("Total de Gols", default=0, blank=True)
    empaths = models.IntegerField("Total de Empates", default=0, blank=True)

    created_by = models.ForeignKey(
        User, related_name="%(app_label)s_%(class)s_created_by", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    updated_by = models.ForeignKey(
        User, related_name="%(app_label)s_%(class)s_updated_by", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    creation_date = models.DateTimeField(_('Data de criação'), null=True, auto_now_add=True)
    last_update = models.DateTimeField(_('Última atualização'), null=True, auto_now=True)
    is_active = models.BooleanField(_('Ativo'), null=False, default=True)

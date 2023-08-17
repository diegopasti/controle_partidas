from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import gettext_lazy as _

from apps.core.models import BaseModel
from apps.entities.models import Company, Area, Group


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
        db_table = "apps_game_players"
        verbose_name = "Jogador"
        verbose_name_plural = "Jogadores"

    user = models.OneToOneField("auth.User", null=True, blank=True, on_delete=models.DO_NOTHING)
    name = models.CharField(_('Nome'), max_length=50, unique=True, blank=False)
    total_bookings = models.IntegerField("Total de Reservas", default=0, blank=True)
    total_matches = models.IntegerField("Total de Partidas", default=0, blank=True)
    total_gols = models.IntegerField("Total de Gols", default=0, blank=True)
    gols_rate = models.DecimalField(
        "Gols por Partida", max_digits=10, decimal_places=2, blank=True, default=0
    )

    best_of_team = models.IntegerField(
        "Melhor do time", default=0, blank=True,
        help_text="Número de vezes em que foi o melhor do time em uma partida")

    best_of_match = models.IntegerField(
        "Melhor da partida", default=0, blank=True,
        help_text="Número de vezes em que foi o melhor da partida"
    )

    bookings = models.ManyToManyField('Booking', verbose_name=_("Reservas"), blank=True)
    matches = models.ManyToManyField('Match', verbose_name=_("Rodadas"), blank=True)

    def __str__(self):
        return self.name


class Booking(BaseModel, ResultFields):
    class Meta:
        db_table = "apps_game_bookings"
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        unique_together = [["company", "area", "date", "hour"]]

    STATUS = (
        ('AGUARDANDO', 'AGUARDANDO'),
        ('CONFIRMADA', 'CONFIRMADA'),
        ('INICIADA', 'INICIADA'),
        ('FINALIZADA', 'FINALIZADA'),
        ('CANCELADA', 'CANCELADA'),
    )

    group = models.ForeignKey("entities.Group", null=True, blank=True, on_delete=models.DO_NOTHING)
    owner = models.ForeignKey(
        "auth.User", related_name="%(app_label)s_%(class)s_owner", null=False, blank=False, on_delete=models.DO_NOTHING
    )
    company = models.ForeignKey("entities.Company", null=False, on_delete=models.DO_NOTHING)
    area = models.ForeignKey("entities.Area", null=False, on_delete=models.DO_NOTHING)
    date = models.DateField(_("Data"), null=False)
    hour = models.TimeField(_('Horário'), null=False)

    status = models.CharField("Status", max_length=10, choices=STATUS, blank=False)
    players = models.ManyToManyField("Player", verbose_name=_('Jogadores'))

    start = models.DateTimeField(_('Início da Partida'))
    finish = models.DateTimeField(_('Término da Partida'))
    duration = models.DurationField(_('Duração Partida'))

    best_player = models.ForeignKey(
        "Player", null=True, blank=True, on_delete=models.DO_NOTHING,
        verbose_name=_("Melhor da Partida"), related_name="%(app_label)s_%(class)s_best_player"
    )

    total_players = models.IntegerField("Total de Jogadores", default=0, blank=True)
    total_teams = models.IntegerField("Total de Times", default=0, blank=True)
    total_matches = models.IntegerField("Total de Partidas", default=0, blank=True)
    total_gols = models.IntegerField("Total de Gols", default=0, blank=True)


class Match(BaseModel):
    class Meta:
        db_table = "apps_game_matches"
        verbose_name = "Jogador"
        verbose_name_plural = "Jogadores"

    start = models.DateTimeField()
    finish = models.DateTimeField()
    duration = models.DurationField()

    first_team = models.ForeignKey(
        "Team", related_name="%(app_label)s_%(class)s_first_team", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    second_team = models.ForeignKey(
        "Team", related_name="%(app_label)s_%(class)s_second_team", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    players = models.ManyToManyField("Player", verbose_name="Jogadores")
    best_player = models.ForeignKey(
        "Player", related_name="%(app_label)s_%(class)s_best_player", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    total_players = models.IntegerField("Total de Jogadores", default=0, blank=True)
    total_teams = models.IntegerField("Total de Times", default=0, blank=True)

    total_rounds = models.IntegerField("Total de Partidas", default=0, blank=True)

    gols = models.IntegerField("Total de Gols", default=0, blank=True)
    victories = models.IntegerField("Total de Vitórias", default=0, blank=True)
    losses = models.IntegerField("Total de Gols", default=0, blank=True)
    empaths = models.IntegerField("Total de Empates", default=0, blank=True)


class Team(BaseModel, ResultFields):
    class Meta:
        db_table = "apps_game_teams"
        verbose_name = "Time"
        verbose_name_plural = "Times"

    match = models.ForeignKey(
        "Match", related_name="%(app_label)s_%(class)s_match", verbose_name="Partida",
        null=True, blank=True, on_delete=models.DO_NOTHING
    )

    code = models.IntegerField("Codigo", default=1, null=True, blank=True)

    name = models.CharField(_('Nome do Time'), max_length=50, blank=False)

    players = models.ManyToManyField("Player", verbose_name="Jogadores")

    best_player = models.ForeignKey(
        "Player", related_name="%(app_label)s_%(class)s_best_player", verbose_name="Melhor jogador do Time",
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


class Gol(BaseModel):
    class Meta:
        db_table = "apps_game_gols"
        verbose_name = "Gol"
        verbose_name_plural = "Gols"

    booking = models.ForeignKey(
        "Booking", null=False, blank=False, on_delete=models.DO_NOTHING, verbose_name=_("Reserva")
    )

    player = models.ForeignKey(
        "Player", null=False, blank=False, on_delete=models.DO_NOTHING, verbose_name=_("Jogador")
    )

    team = models.ForeignKey(
        "Team", null=False, blank=False, on_delete=models.DO_NOTHING, verbose_name=_("Time"),
        related_name="%(app_label)s_%(class)s_team"
    )

    opponent = models.ForeignKey(
        "Team", null=False, blank=False, on_delete=models.DO_NOTHING, verbose_name=_("Oponente"),
        related_name="%(app_label)s_%(class)s_opponent"
    )

    creation_date = models.DateTimeField(_('Horário'), null=True, auto_now_add=True)

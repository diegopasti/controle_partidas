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
    image = models.ImageField(_("Imagem"), upload_to="players", null=True, blank=True)
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

    company = models.ForeignKey(
        "entities.Company", verbose_name="Empresa", null=False, on_delete=models.DO_NOTHING

    )

    area = models.ForeignKey(
        "entities.Area", verbose_name="Quadra ou Campo", null=False, on_delete=models.DO_NOTHING
    )

    group = models.ForeignKey(
        "entities.Group", verbose_name="Grupo", null=False, blank=False, on_delete=models.DO_NOTHING
    )

    owner = models.ForeignKey(
        "auth.User", null=False, blank=False, on_delete=models.DO_NOTHING,
        verbose_name="Responsável", related_name="%(app_label)s_%(class)s_owner",
    )

    date = models.DateField(_("Data"), null=False)
    hour = models.TimeField(_('Horário'), null=False)

    status = models.CharField("Status", max_length=10, choices=STATUS, default="AGUARDANDO", blank=False)
    players = models.ManyToManyField("Player", verbose_name=_('Jogadores'))

    start = models.DateTimeField(_('Início da Reserva'), null=True, blank=True)
    finish = models.DateTimeField(_('Término da Reserva'), null=True, blank=True)
    duration = models.DurationField(_('Duração da Reserva'), null=True, blank=True)

    best_player = models.ForeignKey(
        "Player", null=True, blank=True, on_delete=models.DO_NOTHING,
        verbose_name=_("Melhor da Partida"), related_name="%(app_label)s_%(class)s_best_player"
    )

    total_players = models.IntegerField("Total de Jogadores", default=0, blank=True)
    total_teams = models.IntegerField("Total de Times", default=0, blank=True)
    total_matches = models.IntegerField("Total de Partidas", default=0, blank=True)
    total_gols = models.IntegerField("Total de Gols", default=0, blank=True)

    def __str__(self):
        return f"{self.date} - {self.hour} - {self.company} - {self.group}"


class Match(BaseModel):
    class Meta:
        db_table = "apps_game_matches"
        verbose_name = "Partida"
        verbose_name_plural = "Partidas"

    booking = models.ForeignKey(
        "Booking", null=False, blank=False, on_delete=models.DO_NOTHING,
        verbose_name="Reserva", related_name="%(app_label)s_%(class)s_booking",
    )

    start = models.DateTimeField("Início", null=True, blank=True)
    finish = models.DateTimeField("Término", null=True, blank=True)
    duration = models.DurationField("Duração", null=True, blank=True)

    first_team = models.ForeignKey(
        "Team", null=True, blank=True, on_delete=models.DO_NOTHING,
        verbose_name="Primeiro Time", related_name="%(app_label)s_%(class)s_first_team"
    )

    second_team = models.ForeignKey(
        "Team", null=True, blank=True, on_delete=models.DO_NOTHING,
        verbose_name="Segundo Time", related_name="%(app_label)s_%(class)s_second_team"
    )

    gols = models.IntegerField("Total de Gols", default=0, blank=True)
    first_team_gols = models.IntegerField("Gols do Primeiro Time", default=0, blank=True)
    second_team_gols = models.IntegerField("Gols do Segundo Time", default=0, blank=True)


class Team(BaseModel, ResultFields):
    class Meta:
        db_table = "apps_game_teams"
        verbose_name = "Time"
        verbose_name_plural = "Times"

    booking = models.ForeignKey(
        "Booking", related_name="%(app_label)s_%(class)s_booking", verbose_name="Reserva",
        null=False, blank=False, on_delete=models.DO_NOTHING
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

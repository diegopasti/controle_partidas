from django.contrib.auth.models import User
from django.db import models
from django.utils.text import gettext_lazy as _


class Player(models.Model):
    class Meta:
        db_table = "apps_core_game_player"
        verbose_name = "Jogador"
        verbose_name_plural = "Jogadores"

    name = models.CharField(_('Nome'), max_length=50, blank=False)
    best_of_team = models.IntegerField("Melhor do time", default=0, blank=True)
    best_of_match = models.IntegerField("Melhor da partida", default=0, blank=True)

    matchs = models.ManyToManyField('Match', blank=True)
    total_matchs = models.IntegerField("Total de Partidas", default=0, blank=True)

    rounds = models.ManyToManyField('Round', blank=True)
    total_rounds = models.IntegerField("Total de Rodadas", default=0, blank=True)

    gols = models.IntegerField("Total de Gols", default=0, blank=True)
    gols_rate = models.IntegerField("Gols por Partidas", default=0, blank=True)

    victories = models.IntegerField("Total de Vitórias", default=0, blank=True)
    losses = models.IntegerField("Total de Gols", default=0, blank=True)
    empaths = models.IntegerField("Total de Empates", default=0, blank=True)

    victories_rate = models.DecimalField(
        "Percentual de Vitórias", max_digits=10, decimal_places=2, blank=True
    )

    losses_rate = models.DecimalField(
        "Percentual de Derrotas", max_digits=10, decimal_places=2, blank=True
    )

    empaths_rate = models.DecimalField(
        "Percentual de Empates", max_digits=10, decimal_places=2, blank=True
    )

    created_by = models.ForeignKey(
        User, related_name="%(app_label)s_%(class)s_created_by", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    updated_by = models.ForeignKey(
        User, related_name="%(app_label)s_%(class)s_updated_by", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    creation_date = models.DateTimeField(_('Data de criação'), null=True, auto_now_add=True)
    last_update = models.DateTimeField(_('Última atualização'), null=True, auto_now=True)
    is_active = models.BooleanField(_('Ativo'), null=False, default=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    class Meta:
        db_table = "apps_core_game_team"
        verbose_name = "Time"
        verbose_name_plural = "Times"

    date = models.DateField()

    players = models.ManyToManyField(Player)

    best_player = models.ForeignKey(
        Player, related_name="%(app_label)s_%(class)s_best_player", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    match = models.ForeignKey(
        Player, related_name="%(app_label)s_%(class)s_match", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    total_rounds = models.IntegerField("Total de Rodadas", default=0, blank=True)
    total_round_duration = models.IntegerField("Total de duração das rodadas")
    total_round_average = models.IntegerField("Media de duração das rodadas")

    gols = models.IntegerField("Total de Gols", default=0, blank=True)
    victories = models.IntegerField("Total de Vitórias", default=0, blank=True)
    losses = models.IntegerField("Total de Gols", default=0, blank=True)
    empaths = models.IntegerField("Total de Empates", default=0, blank=True)

    victories_rate = models.DecimalField(
        "Percentual de Vitórias", max_digits=10, decimal_places=2, blank=True
    )

    losses_rate = models.DecimalField(
        "Percentual de Derrotas", max_digits=10, decimal_places=2, blank=True
    )

    empaths_rate = models.DecimalField(
        "Percentual de Empates", max_digits=10, decimal_places=2, blank=True
    )

    created_by = models.ForeignKey(
        User, related_name="%(app_label)s_%(class)s_created_by", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    updated_by = models.ForeignKey(
        User, related_name="%(app_label)s_%(class)s_updated_by", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    creation_date = models.DateTimeField(_('Data de criação'), null=True, auto_now_add=True)
    last_update = models.DateTimeField(_('Última atualização'), null=True, auto_now=True)
    is_active = models.BooleanField(_('Ativo'), null=False, default=True)


class Match(models.Model):
    class Meta:
        db_table = "apps_core_game_match"
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


class Round(models.Model):

    class Meta:
        db_table = "apps_core_game_round"
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

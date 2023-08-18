from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import gettext_lazy as _

from multiselectfield import MultiSelectField

from apps.core.models import BaseModel


class Company(BaseModel):

    class Meta:
        db_table = "apps_entities_companies"
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    name = models.CharField(_('Nome'), max_length=50, blank=False)
    address = models.CharField(_('Endereço'), max_length=200, blank=True)
    location = models.URLField(verbose_name=_('localização'), max_length=255, blank=True)
    state = models.CharField(_('Estado'), max_length=50, blank=True)
    city = models.CharField(_('Cidade'), max_length=50, blank=True)

    def __str__(self):
        return self.name.upper()


class Group(BaseModel):

    class Meta:
        db_table = "apps_entities_groups"
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"

    STATUS = (
        ('ATIVO', 'ATIVO'),
        ('INADIMPLENTE', 'INADIMPLENTE'),
        ('BLOQUEADO', 'BLOQUEADO'),
        ('INATIVO', 'INATIVO'),
    )

    TYPE = (
        ('PRIVADO', 'PRIVADO'),
        ('PUBLICO', 'PUBLICO'),
    )

    DAYS = (
        ('SEGUNDA', 'SEGUNDA'),
        ('TERÇA', 'TERÇA'),
        ('QUARTA', 'QUARTA'),
        ('QUINTA', 'QUINTA'),
        ('SEXTA', 'SEXTA'),
        ('SÁBADO', 'SÁBADO'),
        ('DOMINGO', 'DOMINGO'),
    )

    owner = models.ForeignKey(User, verbose_name="Responsável", null=False, on_delete=models.DO_NOTHING)
    status = models.CharField("Status do Grupo", max_length=20, choices=STATUS, blank=False)
    type = models.CharField("Tipo de Grupo", max_length=20, choices=TYPE, blank=False)
    days = MultiSelectField("Dias de Jogo", choices=DAYS, max_choices=7, max_length=10, null=True, blank=True)
    matches = models.IntegerField("Total de Partidas", default=0, blank=True)

    def __str__(self):
        return self.owner.first_name


class Area(BaseModel):
    class Meta:
        db_table = "apps_entities_areas"
        verbose_name = "Quadra/Campo"
        verbose_name_plural = "Quadras/Campos"

    STATUS = (
        ('ATIVO', 'ATIVO'),
        ('SUSPENSO', 'SUSPENSO'),
        ('INATIVO', 'INATIVO'),
    )

    AREA_TYPES = (
        ('SOCIETY', 'SOCIETY'),
        ('QUADRA', 'QUADRA'),
        ('CAMPO', 'CAMPO'),
    )

    company = models.ForeignKey(Company, null=False, on_delete=models.DO_NOTHING)
    name = models.CharField(_('Nome'), max_length=50, blank=False)
    type = models.CharField("Tipo", max_length=10, choices=AREA_TYPES, blank=False)
    status = models.CharField("Status", max_length=10, choices=STATUS, blank=False)
    price = models.DecimalField("Preço por Hora", max_digits=10, decimal_places=2, null=False, blank=False)

    players = models.IntegerField(
        "Pessoas por Time", default=5, blank=False,
        validators=[MinValueValidator(5), MaxValueValidator(11)],
    )

    def __str__(self):
        message = f"{self.company.name} - {self.type}"
        if self.name:
            message += f" - {self.name}"
        return message

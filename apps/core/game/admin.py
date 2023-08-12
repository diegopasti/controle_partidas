from django.contrib import admin

from apps.core.game.models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):

    fields = (
        'name',
    )

from django import forms

from apps.game.models import Player, Team


class CreationPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ("name",)

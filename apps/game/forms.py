from django import forms

from apps.game.models import Player


class CreationPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ("name",)

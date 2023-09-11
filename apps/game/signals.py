from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.game.models import Player, Team, Booking


@receiver(post_save, sender=Player)
def creation_player(sender, instance, created, **kwargs):
    if created:
        print(f'New Player({instance.pk}) was created.')


@receiver(post_save, sender=Booking)
def creation_booking(sender, instance, created, **kwargs):
    if created:
        instance.group.bookings += 1
        instance.group.save()
        print(f'New Booking ({instance.pk}) was created.')

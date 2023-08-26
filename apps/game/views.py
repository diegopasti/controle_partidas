import datetime

from django.shortcuts import render

from apps.game.models import Team, Match


def game(request, booking):
    """View function for home page of site."""

    teams = Team.objects.filter(booking=booking)

    match = Match.objects.filter(booking=booking).first()
    if not match:
        match = Match()
        match.booking_id = booking
        match.start = datetime.datetime.now()
        match.first_team = teams[0]
        match.second_team = teams[1]
        match.save()

    context = {
        "booking": booking,
        "match": match
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'game.html', context=context)
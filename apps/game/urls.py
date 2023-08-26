from django.urls import path

from apps.game import views

urlpatterns = [
    path('<int:booking>', views.game, name='game'),
]

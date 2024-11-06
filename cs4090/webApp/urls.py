from django.urls import path
from . import views
from .views import index, streak_view, profile_view

urlpatterns = [  # standard method for keeping track of urls.
    path(
        "", views.index, name="index"
    ),  # arguments- urlPath, what happens when u visit that url ex what function will run, give it a name
    # path('calendar/', views.index1.as_view(), name='calendar'),
    path("streak/", streak_view, name="streak_view"),
    path("profile/", profile_view, name="profile"),
]

from django.urls import path
from . import views

urlpatterns = [ #standard method for keeping track of urls. 
    path("",views.index,name="index"), # arguments- urlPath, what happens when u visit that url ex what function will run, give it a name
]
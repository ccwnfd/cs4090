from django.urls import path
from .views.views import create_course, course_list

urlpatterns = [  # standard method for keeping track of urls.
    path("create/", create_course, name="create_course"),  # URL for creating a class
    path("classes/", course_list, name="course_list"),  # URL for listing classes
]

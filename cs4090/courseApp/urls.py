from django.urls import path
from .views.views import create_course, course_list, delete_course


urlpatterns = [  # standard method for keeping track of urls.
    path("create/", create_course, name="create_course"),  # URL for creating a class
    path("classes/", course_list, name="course_list"),  # URL for listing classes
    path(
        "courses/delete/<int:course_id>/", delete_course, name="delete_course"
    ),  # used for deleting a course
]

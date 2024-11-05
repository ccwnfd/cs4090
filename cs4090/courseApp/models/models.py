from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings


class Course(models.Model):
    # ForeignKey to the User model, making each class unique to a user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courses"
    )

    # Fields for class details
    name = models.CharField(max_length=100, help_text="Course name, e.g., Math 101")
    start_time = models.TimeField(help_text="Course start time")
    end_time = models.TimeField(help_text="Course end time")

    course_created_date = models.DateTimeField(
        auto_now_add=True, help_text="Course created date and time"
    )

    DAYS_OF_WEEK_CHOICES = [
        ("Mon", "Monday"),
        ("Tue", "Tuesday"),
        ("Wed", "Wednesday"),
        ("Thu", "Thursday"),
        ("Fri", "Friday"),
        ("Sat", "Saturday"),
        ("Sun", "Sunday"),
    ]
    # Comma-separated list of days (or use another approach for multiple days)
    days_of_week = models.CharField(
        max_length=21,  # Can hold "Mon,Wed,Fri" or similar
        help_text="Days the course meets, e.g., Mon,Wed,Fri",
    )

    def __str__(self):
        return f"{self.name} {self.course_created_date} ({self.days_of_week}) {self.start_time} - {self.end_time}"

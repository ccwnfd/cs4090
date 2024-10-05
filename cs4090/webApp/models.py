from django.db import models
from django.views.generic import TemplateView
from django.utils import timezone


# Create your models here.
class index1(TemplateView):
    template_name = "calendar.html"

class UserStreak(models.Model):
    user_id = models.PositiveIntegerField(unique=True)  # Assuming you use user IDs to identify users
    streak = models.PositiveIntegerField(default=0)
    last_date = models.DateField(default=timezone.now)  # Store the last date the streak was continued

    def __str__(self):
        return f"User {self.user_id}: Streak {self.streak} (Last date: {self.last_date})"
    
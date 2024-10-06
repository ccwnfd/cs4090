from django.db import models
from django.views.generic import TemplateView
from django.utils import timezone
from django.conf import settings


# Create your models here.
class index1(TemplateView):
    template_name = "calendar.html"

class UserStreak(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='streak'
    )  # Directly referencing the User model
    current_streak = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"User {self.user.email}: Streak {self.current_streak} (Last date: {self.last_activity_date})"
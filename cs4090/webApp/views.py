# from django.shortcuts import render'
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.views.generic import TemplateView
from django.utils import timezone
from .models import UserStreak
from accounts.models import User  # Import your custom User model


def index(request):
    return render(request, "welcome.html")


def streak_view(request, email):
    today = timezone.now().date()  # This is already a date object

    # Get the user by their email
    user = get_object_or_404(User, email=email)

    # Now use the user's id to get or create the streak
    user_streak, created = UserStreak.objects.get_or_create(user=user)

    # Ensure that last_activity_date is converted to a date (ignoring time part)
    last_activity_date = user_streak.last_activity_date

    if last_activity_date < today:
        # Streak is broken
        if last_activity_date < today - timezone.timedelta(days=1):
            user_streak.current_streak = 0  # Reset streak
        user_streak.last_activity_date = today  # Store as a date
    else:
        # Streak continues
        user_streak.current_streak += 1
        user_streak.last_activity_date = today  # Store as a date

    user_streak.save()

    context = {
        "streak": user_streak.current_streak,
        "last_activity_date": user_streak.last_activity_date,
    }

    return render(request, "streak.html", context)

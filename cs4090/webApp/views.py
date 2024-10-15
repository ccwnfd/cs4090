# from django.shortcuts import render'
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.views.generic import TemplateView
from django.utils import timezone

from accounts.models.user import User


def index(request):
    return render(request, "welcome.html")


def streak_view(request):
    today = timezone.now().date()

    # Get the currently logged-in user
    user = request.user

    # Get the last activity date and current streak from the user object
    last_activity_date = user.last_activity_date

    if last_activity_date < today:
        # Streak is broken
        if last_activity_date < today - timezone.timedelta(days=1):
            user.current_streak = 0  # Reset streak
        else:
            user.current_streak += 1  # Continue the streak

        # Update last activity date
        user.last_activity_date = today

    user.save()

    context = {
        "streak": user.current_streak,
        "last_activity_date": user.last_activity_date,
    }

    return render(request, "streak.html", context)

#from django.shortcuts import render'
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.conf import settings
from django.views.generic import TemplateView
from django.utils import timezone
from .models import UserStreak
from django.contrib.auth.models import User

def index(request):
    return render(request, 'welcome.html')

# Create your views here.
def streak_view(request, username):
    today = timezone.now().date()  # This is already a date object

    # Get the user by their username
    user = get_object_or_404(User, username=username)

    # Now use the user's id to get or create the streak
    user_streak, created = UserStreak.objects.get_or_create(user_id=user.id)

    # Ensure that last_date is converted to a date (ignoring time part)
    last_date = user_streak.last_date.date() if isinstance(user_streak.last_date, timezone.datetime) else user_streak.last_date

    if last_date < today:
        # Streak is broken
        if last_date < today - timezone.timedelta(days=1):
            user_streak.streak = 0  # Reset streak
        user_streak.last_date = timezone.now()  # Store as full datetime
    else:
        # Streak continues
        user_streak.streak += 1
        user_streak.last_date = timezone.now()  # Store as full datetime

    user_streak.save()

    context = {
        'streak': user_streak.streak,
        'last_date': user_streak.last_date,
    }

    return render(request, 'streak.html', context)
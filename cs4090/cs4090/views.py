from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from calendarapp.models import Event
from django.utils import timezone


def get_streak(user):
    today = timezone.now().date()

    # Get the currently logged-in user

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


class DashboardView(LoginRequiredMixin, View):
    login_url = "accounts:signin"
    template_name = "calendarapp/dashboard.html"

    def get(self, request, *args, **kwargs):
        events = Event.objects.get_all_events(user=request.user)
        running_events = Event.objects.get_running_events(user=request.user)
        latest_events = Event.objects.filter(user=request.user).order_by("-id")[:10]

        # streak info
        get_streak(self.request.user)
        user = self.request.user
        streak = user.current_streak
        last_activity_date = user.last_activity_date

        context = {
            "total_event": events.count(),
            "running_events": running_events,
            "latest_events": latest_events,
            "streak": streak,
            "last_activity_date": last_activity_date,
        }
        return render(request, self.template_name, context)

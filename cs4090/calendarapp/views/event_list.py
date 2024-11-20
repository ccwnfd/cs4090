from django.views.generic import ListView

from calendarapp.models import Event
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class AllEventsListView(LoginRequiredMixin, ListView):
    """All event list views"""

    template_name = "calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_all_events(user=self.request.user)


class RunningEventsListView(LoginRequiredMixin, ListView):
    """Running events list view"""

    template_name = "calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_running_events(user=self.request.user)

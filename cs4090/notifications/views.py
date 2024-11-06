# cs4090/notifications/views.py
from django.views.generic import ListView
from .models import Notification


class NotificationListView(ListView):
    model = Notification
    template_name = "notifications.html"
    context_object_name = "notifications"

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )

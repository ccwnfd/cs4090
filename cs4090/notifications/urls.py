# cs4090/notifications/urls.py
from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("", views.NotificationListView.as_view(), name="list"),
    path(
        "all/", views.NotificationListView.as_view(), name="all"
    ),  # Ensure this matches the name used in reverse
    # other paths...
]

"""
URL configuration for cs4090 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from .views import DashboardView, export_events, import_events

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("admin/", admin.site.urls),
    path(
        "webapp/", include(("webApp.urls", "webApp"), namespace="webApp")
    ),  # Prefix for webApp
    path("", include("accounts.urls")),
    path("", include("calendarapp.urls")),
    path("", include("courseApp.urls")),
    path("import-events/", import_events, name="import_events"),
    path("export-events/", export_events, name="export_events"),
]

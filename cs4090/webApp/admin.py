from django.contrib import admin
from webApp import models


@admin.register(models.UserStreak)
class StreakAdmin(admin.ModelAdmin):
    model = models.UserStreak
    list_display = [
        "current_streak",
        "last_activity_date"
    ]
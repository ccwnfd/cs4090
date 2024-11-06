# from django.shortcuts import render'
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.views.generic import TemplateView
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from accounts.models.user import User
from .forms import ApiKeyForm
from django.contrib import messages
from django.urls import reverse


@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        form = ApiKeyForm(request.POST)
        if form.is_valid():
            api_key = form.cleaned_data["api_key"]
            request.user.canvas_api_key = api_key
            request.user.save()
            messages.success(request, "Your API key was successfully updated.")
            return redirect(
                reverse("webApp:profile")
            )  # Redirect to the profile page or another page
    else:
        form = ApiKeyForm()

    context = {
        "canvas_api_key": user.canvas_api_key,
        "form": form,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }

    return render(request, "profile.html", context)


def index(request):  # also should never be used anymore
    return render(request, "welcome.html")


def streak_view(
    request,
):  # this page can be deleted as long as no issues arise from its deletion
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

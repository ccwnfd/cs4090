from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from courseApp.models.models import Course  # Import Course model directly
from courseApp.forms import CourseForm


@login_required
def create_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course_instance = form.save(commit=False)
            course_instance.user = request.user  # Set the user to the logged-in user
            course_instance.save()
            return redirect(
                "course_list"
            )  # Redirect to the course list view after saving
    else:
        form = CourseForm()

    return render(request, "create_course.html", {"form": form})


@login_required
def course_list(request):
    courses = Course.objects.filter(
        user=request.user
    )  # Get courses for the logged-in user
    return render(request, "course_list.html", {"courses": courses})

from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from courseApp.models.models import Course  # Import Course model directly
from courseApp.forms import CourseForm
from calendarapp.models.event import Event


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


@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        # need to delete every course event
        list_of_events = Event.objects.all()
        for (
            event
        ) in (
            list_of_events
        ):  # Assumes you want to delete pasts events of that class as well, could change later to only delete future events of that class
            if (
                event.title == course.name and course.user == event.user
            ):  # deletes everything with the same title as your couse, thus assuming ur done with everything you manuelly created with the same name
                event.delete()

        course.delete()

        return redirect("course_list")  # Redirect to the course list after deletion
    return render(request, "confirm_delete.html", {"course": course})

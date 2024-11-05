from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Course
from calendarapp.models import Event  # Absolute import without using ..
from datetime import datetime, time, timedelta


def get_next_weekday(start_date, day):
    """
    Get the next occurrence of a specific weekday starting from a given date.

    :param start_date: The date to start from (datetime.date)
    :param day: The day of the week as an integer (0=Monday, 6=Sunday)
    :return: The next occurrence of the specified weekday (datetime.date) or None if not found
    """
    if start_date.weekday() == day:
        return start_date

    print("start date", start_date, "day-", day)
    # Iterate over the next 7 days to find the next occurrence of the specified day
    next_date = None
    for i in range(1, 8):  # Check the next 7 days
        next_day = start_date + timedelta(days=i)
        if next_day.weekday() == day:  # Compare weekday of next_day with the day
            next_date = next_day
            break

    return next_date  # Returns None if not found


@receiver(post_save, sender=Course)
def create_event_for_course(sender, instance, created, **kwargs):
    print("i ran")
    if created:
        # Create an event entry for the course
        course = instance
        print(instance.days_of_week.split(","))
        week_dictionary = {
            "Mon": 0,
            "Tue": 1,
            "Wed": 2,
            "Thu": 3,
            "Fri": 4,
            "Sat": 5,
            "Sun": 6,
        }
        for day in instance.days_of_week.split(
            ","
        ):  # gets each day the class is on and makes an event for it

            course_date = (
                instance.course_created_date.date()
            )  # This gives you just the date
            next_date = get_next_weekday(
                course_date, week_dictionary[day]
            )  # the second paraemater needs to be a num from 0-6 because of built in date.time structure
            if next_date == None:  # should not run unless error happens
                break
            # Combine the date with the start_time and end_time
            start_datetime = datetime.combine(next_date, instance.start_time)
            end_datetime = datetime.combine(next_date, instance.end_time)
            for i in range(
                0, 24
            ):  # assumed course is about 5 months, user can delete course if it ends sooner.
                Event.objects.create(
                    user=instance.user,
                    title=instance.name,
                    start_time=start_datetime + timedelta(days=i * 7),
                    end_time=end_datetime + timedelta(days=i * 7),
                    description="A class you signed up for.",  # assuming Event model has these fields
                    # Add any other fields that are relevant
                )

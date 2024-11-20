from django import forms
from django.core.exceptions import ValidationError
from .models import Course
from accounts.models.user import User
from django.utils import timezone
from courseApp.models import Course  # for test 6 and 7

DAYS_OF_WEEK = [
    ("Mon", "Monday"),
    ("Tue", "Tuesday"),
    ("Wed", "Wednesday"),
    ("Thu", "Thursday"),
    ("Fri", "Friday"),
    ("Sat", "Saturday"),
    ("Sun", "Sunday"),
]

# Define time choices, e.g., every 15 minutes from 7:00 AM to 9:00 PM
TIME_CHOICES = [
    ("07:00", "7:00 AM"),
    ("07:15", "7:15 AM"),
    ("07:30", "7:30 AM"),
    ("07:45", "7:45 AM"),
    ("08:00", "8:00 AM"),
    ("08:15", "8:15 AM"),
    ("08:30", "8:30 AM"),
    ("08:45", "8:45 AM"),
    ("09:00", "9:00 AM"),
    ("09:15", "9:15 AM"),
    ("09:30", "9:30 AM"),
    ("09:45", "9:45 AM"),
    ("10:00", "10:00 AM"),
    ("10:15", "10:15 AM"),
    ("10:30", "10:30 AM"),
    ("10:45", "10:45 AM"),
    ("11:00", "11:00 AM"),
    ("11:15", "11:15 AM"),
    ("11:30", "11:30 AM"),
    ("11:45", "11:45 AM"),
    ("12:00", "12:00 PM"),
    ("12:15", "12:15 PM"),
    ("12:30", "12:30 PM"),
    ("12:45", "12:45 PM"),
    ("13:00", "1:00 PM"),
    ("13:15", "1:15 PM"),
    ("13:30", "1:30 PM"),
    ("13:45", "1:45 PM"),
    ("14:00", "2:00 PM"),
    ("14:15", "2:15 PM"),
    ("14:30", "2:30 PM"),
    ("14:45", "2:45 PM"),
    ("15:00", "3:00 PM"),
    ("15:15", "3:15 PM"),
    ("15:30", "3:30 PM"),
    ("15:45", "3:45 PM"),
    ("16:00", "4:00 PM"),
    ("16:15", "4:15 PM"),
    ("16:30", "4:30 PM"),
    ("16:45", "4:45 PM"),
    ("17:00", "5:00 PM"),
    ("17:15", "5:15 PM"),
    ("17:30", "5:30 PM"),
    ("17:45", "5:45 PM"),
    ("18:00", "6:00 PM"),
    ("18:15", "6:15 PM"),
    ("18:30", "6:30 PM"),
    ("18:45", "6:45 PM"),
    ("19:00", "7:00 PM"),
    ("19:15", "7:15 PM"),
    ("19:30", "7:30 PM"),
    ("19:45", "7:45 PM"),
    ("20:00", "8:00 PM"),
    ("20:15", "8:15 PM"),
    ("20:30", "8:30 PM"),
    ("20:45", "8:45 PM"),
    ("21:00", "9:00 PM"),
]


class CourseForm(forms.ModelForm):
    days_of_week = forms.MultipleChoiceField(
        choices=DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Course Days",
    )
    start_time = forms.ChoiceField(choices=TIME_CHOICES, label="Start Time")
    end_time = forms.ChoiceField(choices=TIME_CHOICES, label="End Time")

    class Meta:
        model = Course
        fields = ["name", "start_time", "end_time", "days_of_week"]

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        temp_name = cleaned_data.get("name")

        # Validate that the end time is after the start time
        if start_time and end_time and end_time <= start_time:
            raise ValidationError("End time must be after start time.")

        foundClass = Course.objects.filter(
            name=temp_name
        )  # Makes sure class names are not duplicates
        if foundClass.exists():
            raise ValidationError("Another class already has this name.")

        # Join selected days into a comma-separated string for storage
        cleaned_data["days_of_week"] = ",".join(cleaned_data.get("days_of_week", []))
        return cleaned_data

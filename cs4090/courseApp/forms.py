from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import Course
from accounts.models.user import User


DAYS_OF_WEEK = [
    ("Mon", "Monday"),
    ("Tue", "Tuesday"),
    ("Wed", "Wednesday"),
    ("Thu", "Thursday"),
    ("Fri", "Friday"),
    ("Sat", "Saturday"),
    ("Sun", "Sunday"),
]


class CourseForm(forms.ModelForm):
    days_of_week = forms.MultipleChoiceField(
        choices=DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Course Days",
    )

    class Meta:
        model = Course
        fields = ["name", "start_time", "end_time", "days_of_week"]

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        # Validate that the end time is after the start time
        if start_time and end_time and end_time <= start_time:
            raise ValidationError("End time must be after start time.")

        # Join selected days into a comma-separated string for storage
        cleaned_data["days_of_week"] = ",".join(cleaned_data.get("days_of_week", []))

        return cleaned_data

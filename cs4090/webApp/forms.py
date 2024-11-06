# webApp/forms.py
from django import forms
import requests


class ApiKeyForm(forms.Form):
    api_key = forms.CharField(
        label="New API Key",
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter your new API key"}
        ),
    )

    def clean_api_key(self):
        api_key = self.cleaned_data["api_key"]

        # Make a sample request to the Canvas API to validate the API key
        # Replace this URL with a valid endpoint for testing, e.g., user profile
        test_url = "https://umsystem.instructure.com/api/v1/calendar_events"
        headers = {"Authorization": f"Bearer {api_key}"}

        try:
            response = requests.get(test_url, headers=headers)
            if response.status_code != 200:
                raise forms.ValidationError(
                    "Invalid API key. Please check and try again."
                )
        except requests.RequestException:
            raise forms.ValidationError(
                "Could not validate the API key. Please try again."
            )

        return api_key

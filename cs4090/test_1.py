from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from webApp.views import streak_view
from accounts.models.user import User

from calendarapp.models import Event
from calendarapp.forms import EventForm


class UserTestCase(TestCase):
    def setUp(self):
        """Set up a user and streak for testing."""
        # Create a user using the custom User model's manager
        self.user = User.objects.create_user(
            email="testuser@example.com", password="Fake@1234", is_active=True
        )
        # Set up streak-related fields on the user (assumed integrated into the User model)
        self.user.current_streak = 100
        self.user.last_activity_date = timezone.now().date()
        self.user.save()

    def test_user_creation(self):
        """Test that the user was created properly."""
        user = User.objects.get(email="testuser@example.com")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.check_password("Fake@1234"))
        self.assertEqual(user.current_streak, 100)
        self.assertEqual(user.last_activity_date, timezone.now().date())

    def test_signup_form_submission(self):  # tests the sign up page extensivly
        # Makes sure the sign up page is still working---------------------------------------------------------
        url = reverse("accounts:signup")
        response = self.client.post(
            url,
            {
                "first_name": "Test",
                "last_name": "User",
                "email": "testuser1@example.com",
                "password1": "ComplexP@ssword123",
                "password2": "ComplexP@ssword123",
            },
            follow=True,
        )

        # Check for a successful redirect to the 'signin' page
        self.assertRedirects(response, reverse("accounts:signin"))
        self.assertTrue(User.objects.filter(email="testuser1@example.com").exists())

        # second part of test for invalid password--------------------------------------------------------------------
        response = self.client.post(
            url,
            {
                "first_name": "Test",
                "last_name": "User",
                "email": "testuser2@example.com",
                "password1": "12",
                "password2": "12",
            },
        )

        # Reload the form to check for errors after submission
        form = response.context["form"]
        self.assertFalse(form.is_valid(), "Form should be invalid with a weak password")
        self.assertIn(
            "password1", form.errors, "Password validation should trigger an error"
        )

        # Third test for non matching passwords----------------------------------------------------------------------------------------------
        response = self.client.post(
            url,
            {
                "first_name": "Test",
                "last_name": "User",
                "canvas_api_key": "none",
                "email": "testuser3@example.com",
                "password1": "Complex@Password123",
                "password2": "Complexx@password123",
            },
        )

        # Reload the form to check for errors after submission
        form = response.context["form"]
        # print("Form errors:", form.errors)
        self.assertFalse(form.is_valid(), "Form does not have matching passwords")

        # User is already in database Error----------------------------------------------------------------------------------------------------
        response = self.client.post(
            url,
            {
                "first_name": "Test",
                "last_name": "User",
                "canvas_api_key": "none",
                "email": "testuser1@example.com",
                "password1": "Complex@Password1234",
                "password2": "Complex@Password1234",
            },
        )

        # Reload the form to check for errors after submission
        form = response.context["form"]
        # print("Form errors:", form.errors)
        self.assertFalse(form.is_valid(), "Email already exists")

    def test_signin_form_submission(self):  # tests the sign in page extensivly
        # Makes sure the sign in page is still working---------------------------------------------------------
        url = reverse("accounts:signin")

        response = self.client.post(
            url,
            {
                "email": "testuser@example.com",
                "password": "Fake@1234",
            },
            follow=True,
        )

        # Check if the user is authenticated
        self.assertTrue(
            response.wsgi_request.user.is_authenticated,
            "User should be logged in after providing valid credentials",
        )

    def test_bad_signin_attempts(self):  # tests the sign in page extensivly
        url = reverse("accounts:signin")
        # Test with wrong password--------------------------------------------------------------------------------------------------------------
        response = self.client.post(
            url,
            {
                "email": "testuser@example.com",
                "password": "Fake@12345",
            },
            follow=True,
        )

        # Check if the user is authenticated
        self.assertFalse(
            response.wsgi_request.user.is_authenticated, "User should not be logged in"
        )
        # Test with wrong email--------------------------------------------------------------------------------------------------------------
        response = self.client.post(
            url,
            {
                "email": "testuser@example.comw",
                "password": "Fake@1234",
            },
            follow=True,
        )

        # Check if the user is authenticated
        self.assertFalse(
            response.wsgi_request.user.is_authenticated, "User should not be logged in"
        )

    def test_event_form_valid(self):  # Makes sure events can still be added.
        """Test that the EventForm is valid and creates an Event."""
        # Data to submit through the form
        form_data = {
            "title": "Test Event",
            "description": "This is a test event.",
            "start_time": "2024-11-04T15:30",
            "end_time": "2024-11-04T16:30",
        }

        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())  # Check if form is valid

        # Save the form and check if an event was created
        event = form.save(commit=False)
        event.user = self.user  # Assign the user to the event
        event.save()

        # Ensure the event was saved to the database
        self.assertEqual(Event.objects.count(), 1)
        event_in_db = Event.objects.first()
        self.assertEqual(event_in_db.title, "Test Event")
        self.assertEqual(event_in_db.description, "This is a test event.")
        self.assertEqual(event_in_db.user, self.user)

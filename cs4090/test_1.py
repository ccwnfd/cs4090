from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from webApp.views import streak_view
from accounts.models.user import User

from calendarapp.models import Event  # for test 5
from calendarapp.forms import EventForm

from courseApp.models import Course  # for test 6 and 7
from courseApp.forms import CourseForm


class UserTestCase(TestCase):
    def setUp(self):
        """Set up a user and streak for testing."""
        # Create a user using the custom User model's manager
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="Fake@1234",
            first_name="Bob",
            last_name="dan",
            is_active=True,
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

    def test_course_form_valid(self):  # Makes sure classes can still be added.
        """Test that the EventForm is valid and creates an Event."""
        # Data to submit through the form
        form_data = {
            "name": "Driving class",
            "start_time": "07:00",
            "end_time": "08:00",
            "days_of_week": ["Mon", "Wed", "Fri"],
        }

        form = CourseForm(data=form_data)
        self.assertTrue(form.is_valid())  # Check if form is valid

        # Save the form and check if an event was created
        course = form.save(commit=False)
        course.user = self.user  # Assign the user to the event
        course.save()

        # Ensure the event was saved to the database
        self.assertEqual(Course.objects.count(), 1)
        course_in_db = Course.objects.first()
        self.assertEqual(course_in_db.name, "Driving class")
        self.assertEqual(course_in_db.user, self.user)
        self.assertEqual(course_in_db.days_of_week, "Mon,Wed,Fri")

    def test_course_form_invalid_time(
        self,
    ):  # Makes sure classes with bad times are not added
        """Test that the CourseForm doesnt make bad courses"""
        # Data to submit through the form
        form_data = {
            "name": "Driving class2",
            "start_time": "07:00",
            "end_time": "06:00",
            "days_of_week": ["Mon", "Wed", "Fri"],
        }

        form = CourseForm(data=form_data)
        self.assertFalse(form.is_valid())  # Check if form is valid

    def test_course_form_invalid_name(self):  # Makes sure classes have unique names
        """Test that the EventForm is valid and creates an Event."""
        # Data to submit through the form
        form_data = {
            "name": "Driving class",
            "start_time": "07:00",
            "end_time": "08:00",
            "days_of_week": ["Mon", "Wed", "Fri"],
        }

        form = CourseForm(data=form_data)
        self.assertTrue(form.is_valid())  # Check if form is valid

        # Save the form and check if an event was created
        course = form.save(commit=False)
        course.user = self.user  # Assign the user to the event
        course.save()

        # Ensure the event was saved to the database
        self.assertEqual(Course.objects.count(), 1)
        course_in_db = Course.objects.first()
        self.assertEqual(course_in_db.name, "Driving class")
        self.assertEqual(course_in_db.user, self.user)
        self.assertEqual(course_in_db.days_of_week, "Mon,Wed,Fri")

        form_data = {
            "name": "Driving class",
            "start_time": "08:00",
            "end_time": "09:00",
            "days_of_week": ["Mon", "Wed"],
        }

        form = CourseForm(data=form_data)
        self.assertFalse(form.is_valid())  # Check if form is valid


class PageAccessTest(TestCase):  # these cases makes sure pages are viewable
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="Fake@1234",
            first_name="Bob",
            last_name="dan",
            is_active=True,
        )

        self.classes_url = reverse("course_list")
        self.create_course_url = reverse("create_course")
        self.dashboard_url = reverse("dashboard")
        self.calendar_url = reverse("calendarapp:calendar")
        self.all_events_url = reverse("calendarapp:all_events")
        self.running_events_url = reverse("calendarapp:running_events")
        self.profile_url = reverse("webApp:profile")
        self.settings_url = reverse("webApp:settings")

    def test_classes_list_page_access_for_logged_in_user(self):
        # Log in the user
        self.client.login(email="testuser@example.com", password="Fake@1234")

        # Access the /classes/ page
        response = self.client.get(self.classes_url)

        # Check that the logged-in user can access the page
        self.assertEqual(response.status_code, 200)

    def test_classes_list_page_access_for_non_logged_in_user(self):
        # Access the /classes/ page without logging in
        response = self.client.get(self.classes_url)

        # Check that the non-logged-in user is redirected
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertNotEqual(response.status_code, 200)
        # self.assertRedirects(response, f"{reverse('accounts:signin')}?next={self.classes_url}") # currently page not found issue happens no redirect

    def test_classes_create_page_access_for_logged_in_user(
        self,
    ):  # tests if you can view create couses pages
        # Log in the user
        self.client.login(email="testuser@example.com", password="Fake@1234")

        # Access the /classes/ page
        response = self.client.get(self.create_course_url)

        # Check that the logged-in user can access the page
        self.assertEqual(response.status_code, 200)

    def test_classes_create_page_access_for_non_logged_in_user(self):
        response = self.client.get(self.create_course_url)

        # Check that the non-logged-in user is redirected
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertNotEqual(response.status_code, 200)
        # self.assertRedirects(response, f"{reverse('accounts:signin')}?next={self.classes_url}") # currently page not found issue happens no redirect

    def test_dashboard_user_logged_in(
        self,
    ):  # tests if you can view create couses pages
        # Log in the user
        self.client.login(email="testuser@example.com", password="Fake@1234")

        # Access the /classes/ page
        response = self.client.get(self.dashboard_url)

        # Check that the logged-in user can access the page
        self.assertEqual(response.status_code, 200)

    def test_dashboard_user_logged_out(self):
        response = self.client.get(self.dashboard_url)

        # Check that the non-logged-in user is redirected
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertNotEqual(response.status_code, 200)
        # self.assertRedirects(response, f"{reverse('accounts:signin')}?next={self.classes_url}") # currently page not found issue happens no redirect

    def test_calendar_user_logged_in(self):
        # Log in the user
        self.client.login(email="testuser@example.com", password="Fake@1234")

        # Access the /classes/ page
        response = self.client.get(self.calendar_url)

        # Check that the logged-in user can access the page
        self.assertEqual(response.status_code, 200)

    def test_calendar_user_logged_out(self):
        response = self.client.get(self.calendar_url)

        # Check that the non-logged-in user is redirected
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertNotEqual(response.status_code, 200)
        # self.assertRedirects(response, f"{reverse('accounts:signin')}?next={self.classes_url}") # currently page not found issue happens no redirect

    def test_event_list_user_logged_in(self):
        # Log in the user
        self.client.login(email="testuser@example.com", password="Fake@1234")

        # Access the /classes/ page
        response = self.client.get(self.all_events_url)

        # Check that the logged-in user can access the page
        self.assertEqual(response.status_code, 200)

        # Access the /classes/ page
        response = self.client.get(self.running_events_url)

        # Check that the logged-in user can access the page
        self.assertEqual(response.status_code, 200)

    def test_event_list_user_logged_out(self):
        response = self.client.get(self.all_events_url)

        # Check that the non-logged-in user is redirected
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertNotEqual(response.status_code, 200)
        # self.assertRedirects(response, f"{reverse('accounts:signin')}?next={self.classes_url}") # currently page not found issue happens no redirect

        response = self.client.get(self.running_events_url)

        # Check that the non-logged-in user is redirected
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertNotEqual(response.status_code, 200)
        # self.assertRedirects(response, f"{reverse('accounts:signin')}?next={self.classes_url}") # currently page not found issue happens no redirect

    def test_profile_user_logged_in(self):
        # Log in the user
        self.client.login(email="testuser@example.com", password="Fake@1234")

        # Access the /classes/ page
        response = self.client.get(self.profile_url)

        # Check that the logged-in user can access the page
        self.assertEqual(response.status_code, 200)

    def test_profile_user_logged_out(self):
        response = self.client.get(self.profile_url)

        # Check that the non-logged-in user is redirected
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertNotEqual(response.status_code, 200)
        # self.assertRedirects(response, f"{reverse('accounts:signin')}?next={self.classes_url}") # currently page not found issue happens no redirect

    def test_event_list_user_logged_out(self):
        response = self.client.get(self.all_events_url)

        # Check that the non-logged-in user is redirected
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertNotEqual(response.status_code, 200)
        # self.assertRedirects(response, f"{reverse('accounts:signin')}?next={self.classes_url}") # currently page not found issue happens no redirect

        response = self.client.get(self.running_events_url)

        # Check that the non-logged-in user is redirected
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertNotEqual(response.status_code, 200)
        # self.assertRedirects(response, f"{reverse('accounts:signin')}?next={self.classes_url}") # currently page not found issue happens no redirect

    def test_settings_user_logged_in(self):
        # Log in the user
        self.client.login(email="testuser@example.com", password="Fake@1234")

        # Access the /classes/ page
        response = self.client.get(self.settings_url)

        # Check that the logged-in user can access the page
        self.assertEqual(response.status_code, 200)

    def test_settings_user_logged_out(self):
        response = self.client.get(self.settings_url)

        # Check that the non-logged-in user is redirected
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertNotEqual(response.status_code, 200)
        # self.assertRedirects(response, f"{reverse('accounts:signin')}?next={self.classes_url}") # currently page not found issue happens no redirect

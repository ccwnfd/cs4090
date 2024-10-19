from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from webApp.views import streak_view
from accounts.models.user import User


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

    def test_streak_view(self):
        """Test the streak view for the created user."""
        # Simulate a logged-in user with RequestFactory
        factory = RequestFactory()
        path = reverse("streak_view")  # Ensure the name matches your URL pattern
        request = factory.get(path)

        # Simulate the logged-in user
        request.user = self.user

        # Call the streak view
        response = streak_view(request)

        # Assert that the view returns a 200 status code
        self.assertEqual(response.status_code, 200)

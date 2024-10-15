import pytest    

from cs4090.webApp.models import UserStreak 
from cs4090.webApp.views import streak_view
from django.test import RequestFactory
from django.urls import reverse
from django.utils import timezone

# test for the UserStreak database object
@pytest.mark.django_db #give test access to database  
def test_contact_create():    
    # Create dummy data       
    current_date = timezone.now
    dummy_streak = UserStreak.objects.create(current_streak=100, last_activity_date=current_date)    
    # Assert the dummy data saved as expected       
    assert dummy_streak.current_streak==100      
    assert dummy_streak.last_activity_date==current_date


# test for the streak view
@pytest.mark.django_db 
def test_view():
    path = reverse("streak")
    # get the path for the streak view
    request = RequestFactory().get(path) 
    response = streak_view(request)
    # assert status code from requesting the view is 200 (OK success status response code)
    assert response.status_code == 200 

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from calendarapp.models import Event
from datetime import datetime, timedelta
import requests
import json
import sqlite3


# Import event function
def import_events_from_json(user_id, filename):

    # Parse the incoming JSON data
    try:
        with open(filename, "r") as json_data:
            events = json.loads(json_data)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return {"error": "Invalid JSON data"}

    # Connect to the database
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()

    # Insert events into the event table
    for event in events:
        try:
            # Insert or replace event data
            cur.execute(
                """
                INSERT OR REPLACE INTO calendarapp_event (user_id, title, description, start_time, end_time)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    user_id,
                    event["title"],
                    event["description"],
                    event["start_time"],
                    event["end_time"],
                ),
            )
        except sqlite3.Error as e:
            print(f"Error inserting event: {e}")
            continue

    # Commit the changes and close the connection
    con.commit()
    con.close()

    return {"success": "Events imported successfully"}


# create function to respond to import javascript query
@csrf_exempt
def import_events(request):
    if request.method == "GET":
        import_events_from_json()
        return JsonResponse({"success": "Event data successfully imported"}, status=200)
    return JsonResponse({"error": "Invalid request"}, status=400)


# Export event function


def export_events_to_json(user_id):

    # Connect to the database
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()

    # Select events for the specific user from the event table
    cur.execute(
        """
        SELECT title, description, start_time, end_time
        FROM calendarapp_event
        WHERE user_id = ?
    """,
        (user_id,),
    )

    # Fetch all the events data for the user
    events_data = cur.fetchall()

    # Convert the events data into a list of dictionaries
    events = [
        {
            "title": event[0],
            "description": event[1],
            "start_time": event[2],
            "end_time": event[3],
        }
        for event in events_data
    ]

    # Convert the list of events to JSON with indentation for readability
    events_json = json.dumps(events, indent=2)

    # Close the connection
    con.close()

    return events_json


# create function to respond to export javascript query
@csrf_exempt
def export_events(request):
    if request.method == "GET":
        json_data = export_events_to_json()
        return JsonResponse(json.loads(json_data), safe=False, status=200)
    return JsonResponse({"error": "Invalid request"}, status=400)


def get_streak(user):
    today = timezone.now().date()

    # Get the currently logged-in user
    # Get the last activity date and current streak from the user object
    last_activity_date = user.last_activity_date

    if last_activity_date < today:
        # Streak is broken
        if last_activity_date < today - timezone.timedelta(days=1):
            user.current_streak = 0  # Reset streak
        else:
            user.current_streak += 1  # Continue the streak

        # Update last activity date
        user.last_activity_date = today

    user.save()


def adding_events_from_canvas(user):
    if user.canvas_api_key != None:
        # Define the URL for the Canvas API endpoint
        url = "https://umsystem.instructure.com/api/v1/calendar_events"  # This will only work for MS&T
        # Set up the headers, including the access token
        headers = {"Authorization": f"Bearer {user.canvas_api_key}"}  #
        # Define the date range for retrieving events
        start_date = (
            datetime.now() - timedelta(days=1)
        ).isoformat()  # Looks one day behind
        end_date = (
            datetime.now() + timedelta(days=30)
        ).isoformat()  # 30 days in the future
        # Add date parameters to retrieve events in the future
        params = {"start_date": start_date, "end_date": end_date}
        # Make the GET request to the API
        response = requests.get(url, headers=headers, params=params)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse and print the JSON response
            info = response.json()

            for event in info:
                temp_title = event["title"]
                temp_description = event["description"]
                if temp_description == None:
                    temp_description = "No description"
                temp_start_time = datetime.fromisoformat(
                    event["start_at"].replace("Z", "+00:00")
                )  # ensure proper time zone formats
                temp_end_time = datetime.fromisoformat(
                    event["end_at"].replace("Z", "+00:00")
                )

                existing_event = Event.objects.filter(
                    user=user,
                    title=temp_title,
                    start_time=temp_start_time,
                    end_time=temp_end_time,
                ).first()

                if not existing_event:
                    new_event = Event(
                        user=user,
                        title=temp_title,
                        description=temp_description,
                        start_time=temp_start_time,
                        end_time=temp_end_time,
                    )
                    new_event.save()

        else:
            print(f"Failed to retrieve data: ...")


class DashboardView(LoginRequiredMixin, View):
    login_url = "accounts:signin"
    template_name = "calendarapp/dashboard.html"

    def get(self, request, *args, **kwargs):
        # Add events from canvas here.--------------------------------------------
        adding_events_from_canvas(self.request.user)
        # ----------------------------------------------------------------

        events = Event.objects.get_all_events(user=request.user)
        running_events = Event.objects.get_running_events(user=request.user)
        latest_events = Event.objects.filter(user=request.user).order_by("-id")[:10]

        # streak info
        get_streak(self.request.user)
        user = self.request.user
        streak = user.current_streak
        last_activity_date = user.last_activity_date

        context = {
            "total_event": events.count(),
            "running_events": running_events,
            "latest_events": latest_events,
            "streak": streak,
            "last_activity_date": last_activity_date,
        }
        return render(request, self.template_name, context)

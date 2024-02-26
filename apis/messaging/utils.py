 
import jwt
import json
import logging
import requests
from time import time
from zoomus import ZoomClient
from django.conf import settings



logger = logging.getLogger("myLogger")


def generateToken():
        url = 'https://zoom.us/oauth/token'
        API_KEY = settings.ZOOM_CLIENT_ID
        API_SEC = settings.ZOOM_CLIENT_SECRET
        ACCOUNT_ID = settings.ZOOM_ACCOUNT_ID
        payload = {
            'grant_type': 'account_credentials',
            'account_id' : ACCOUNT_ID,
            'client_id': API_KEY,
            'client_secret': API_SEC,
        }

        response = requests.post(url, data=payload)
        access_token = response.json().get('access_token')
        
        return access_token


def createMeeting(topic, start_time, duration):
    token = generateToken()
    headers = {'authorization': 'Bearer ' + token,
               'content-type': 'application/json'
               }
    print(headers)
    
    # create json data for post requests
    meetingdetails = {"topic": topic,
                    "type": 2,
                    "start_time": start_time, #"2019-06-14T10: 21: 57",
                    "duration": duration, #"45",
                    "timezone": "Africa/Douala",
                    "agenda": topic,
    
                    "recurrence": {"type": 1,
                                    "repeat_interval": 1
                                    },
                    "settings": {"host_video": "true",
                                "participant_video": "true",
                                "join_before_host": "False",
                                "mute_upon_entry": "False",
                                "watermark": "true",
                                "audio": "voip",
                                "auto_recording": "cloud"
                                }
                    }
    
    response = requests.post(
        f'https://api.zoom.us/v2/users/me/meetings',
        headers=headers, data=json.dumps(meetingdetails))
 
    print("\n creating zoom meeting ... \n")
    print(response)
    if response.status_code == 201:
        # y = json.loads(response.text)
        # join_URL = y["join_url"]
        # meetingPassword = y["password"]
        # print(
        # f'\n here is your zoom meeting link {join_URL} and your \
        # password: "{meetingPassword}"\n')
        return response.json()
    else:
        # Print the error details if the request fails
        logger.error( f"Failed to schedule meeting. Status code: {response.status_code}" , extra={ 'user': 'Anonymous' } )
        print(f"Failed to schedule meeting. Status code: {response.status_code}")
        print(response.text)
        return None
    # print(r.text)
    # converting the output into json and extracting the details
    y = json.loads(response.text)
    join_URL = y["join_url"]
    meetingPassword = y["password"]
 
    print(
        f'\n here is your zoom meeting link {join_URL} and your \
        password: "{meetingPassword}"\n')


def create_zoom_meeting(topic, start_time, duration):
    api_key = settings.ZOOM_CLIENT_ID
    api_secret = settings.ZOOM_CLIENT_SECRET
    api_account_id = settings.ZOOM_ACCOUNT_ID

    client = ZoomClient(api_key, api_secret, api_account_id)
    print(client)

    # Create a meeting
    meeting_response = client.meeting.create(user_id='me',
                                             topic=topic,
                                             type=2,  # 2 for scheduled meeting
                                             start_time=start_time,
                                             duration_in_minutes=duration)
    print(meeting_response)
    return meeting_response



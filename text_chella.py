from pymongo import MongoClient
import os
import datetime
import time
import emoji
from twilio.base import exceptions
from twilio.rest import Client
from reports import send_daily_report, send_new_sub_report


def get_twilio_client():
    username = os.environ['TWILIO_SID']  # Auth_SID
    password = os.environ['TWILIO_TOKEN']  # Auth_Token
    return Client(username, password)


def get_connection():
    user = os.environ['MLAB_USER']
    password = os.environ['MLAB_PW']
    mlab_url = os.environ['MLAB_LINK']
    return MongoClient("mongodb://"+user+":"+password+"@"+mlab_url)


def text_chella():
    twilio_client = get_twilio_client()
    db_client = get_connection()
    db = db_client['textchella']
    days = days_until_coachella()

    todays_artist = get_todays_artist()
    users = db.Users.find()
    num_users = users.count()
    send_daily_report(num_users, days)

    for idx, user in enumerate(users):
        try:  # Try to send message
            twilio_client.messages.create(to=user["UserNumber"], from_="+16505390580", body=todays_artist)
            print("Send Success. Message #: " + str(idx))  # Print success
        except exceptions.TwilioRestException or exceptions.TwilioException:  # Catch twilio exception if occured
            print("Exception Caught. Phone #: " + str(user) + ". Message #: " + str(idx))  # Print exception

        time.sleep(1)  # https://stackoverflow.com/questions/45883737/503-error-while-trying-to-send-sms-with-twilio


def get_todays_artist(new_user=False):
    db_client = get_connection()
    db = db_client['textchella']
    days = days_until_coachella()
    result = db.ArtistInfo.find({
        "Day": str(days)
    })

    artist_name = ""
    artist_genre = ""
    artist_description = ""
    artist_link = ""

    for artist in result:
        artist_name = artist["ArtistName"]
        artist_genre = artist["ArtistGenre"]
        artist_description = artist["ArtistDescription"]
        artist_link = artist["SpotifyLink"]

    sun_emoji = emoji.emojize(' :sun_with_face:')
    tree_emoji = emoji.emojize(' :palm_tree:')
    message = sun_emoji + "\n\n" + str(days) + " days until the festival!" + tree_emoji + "\n\n" + "Here is your song of the day!" + "\n\n" + "Artist Name: " + artist_name + "\n\n" + "Genre: " + artist_genre + "\n\n" + "Bio: " + artist_description + "\n\n" + "Featured Song: \n" + artist_link

    if new_user:
        return "Welcome to TextChella!" + message

    return "Good Morning!" + message


def days_until_coachella():
    date_of_chella = datetime.datetime(2019, 4, 12, 0, 0)
    todays_date = datetime.datetime.now()
    diff = date_of_chella - todays_date
    return diff.days


def load_analytics(num_users):
    days = days_until_coachella()
    db_client = get_connection()
    db = db_client['textchella']
    db.Analytics.insert({
        "NumUsers": str(num_users),
        "days": str(days)
    })


def is_user(phone_number):
    db_client = get_connection()
    db = db_client['textchella']
    result = db.Users.find({"UserNumber": phone_number})

    if result.count() == 0:
        return False
    else:
        return True


def subscribe(phone_number):
    db_client = get_connection()
    user_collection = db_client['textchella']['Users']
    user_collection.insert({
        "UserNumber": phone_number
    })

    send_new_sub_report(phone_number)
    return get_todays_artist(new_user=True)


def delete_user(phone_number):
    db_client = get_connection()
    db = db_client['textchella']
    db.Users.delete_one({
        "UserNumber": phone_number
    })

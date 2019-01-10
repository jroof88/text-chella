from pymongo import MongoClient
import os
import datetime
import emoji
from datetime import date
from twilio.rest import Client

username = os.environ['TWILIO_SID'] #Auth_SID
password = os.environ['TWILIO_TOKEN']	#Auth_Token
client = Client(username, password)

def get_connection():
	user = os.environ['MLAB_USER']
	password = os.environ['MLAB_PW']
	mlab_url = os.environ['MLAB_LINK']
	return MongoClient("mongodb://"+user+":"+password+"@"+mlab_url)

    
def text_chella():
	# dbClient = get_connection()
	# db = dbClient['textchella']
	# todays_artist = get_todays_artist()
	# users = db.Users.find()
	# load_analytics(users.count())
	# for user in users:
	# 	client.messages.create(to=user["UserNumber"], from_="+16505390580", body=todays_artist)

	# test_users = {
 #    	"_id" : "Sanjay"
 #    	"UserNumber": "+19164708305"
	# }

	# client.messages.create(to=test_users["UserNumber"], from_="+16505390580", body= "Hello World")



		
def get_todays_artist(new_user=False):
	dbClient = get_connection()
	db = dbClient['textchella']
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
		return "Welcome to Text Chella!" + message
		
	return "Good Morning!" + message


	
def days_until_coachella():
	date_of_chella = datetime.datetime(2018, 4, 14, 0, 0)
	todays_date = datetime.datetime.now()
	diff = date_of_chella - todays_date
	return diff.days

def load_analytics(num_users):
	days = days_until_coachella()
	dbClient = get_connection()
	db = dbClient['textchella']
	db.Analytics.insert({
		"NumUsers": str(num_users),
		"days": str(days)
	})

def is_user(phone_number):
	client = get_connection()
	db = client['textchella']
	result = db.Users.find({"UserNumber": phone_number})

	if result.count() == 0:
		return False
	else:
		return True


    
def subscribe(phone_number):
	# dbClient = get_connection()
	# user_collection = dbClient['textchella']['Users']
	# user_collection.insert({
	# 	"UserNumber": phone_number
	# })

	# new_subscriber_message = "New Subscriber! :" + str(phone_number)
	# client.messages.create(to="+19164708305", from_="+16505390580", body=new_subscriber_message)
	# client.messages.create(to="+12038565701", from_="+16505390580", body=new_subscriber_message) 
	# return get_todays_artist(new_user=True)

	print(phone_number)
	return "Hello new user!"



	
def delete_user(phone_number):
	dbClient = get_connection()
	db = dbClient['textchella']
	result = db.Users.delete_one({
		"UserNumber": phone_number
	})
	





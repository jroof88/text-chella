from pymongo import MongoClient
from twilio.rest import Client

username = 'ACbdc10bdbf54d948807715fde6396ad07' #Auth_SID
password = '62bdcbe9eff5290f18df55601b33e9f9'	#Auth_Token
client = Client(username, password)

def get_connection():
	user = "textchella"
	password = "textchella123"
	mlab_url = "ds261678.mlab.com:61678/textchella"
	return MongoClient("mongodb://"+user+":"+password+"@"+mlab_url)
    

def text_chella():
	dbClient = get_connection()
	db = dbClient['textchella']
	result = db.ArtistInfo.aggregate(
		[{'$sample' : {'size':1}}]
	)

	artist_name =""
	artist_genre =""
	artist_description =""
	artist_link =""
	doc_id =""

	for artist in result:
		artist_name =artist["ArtistName"]
		artist_genre =artist["ArtistGenre"]
		artist_description = artist["ArtistDescription"]
		artist_link = artist["SpotifyLink"]
		doc_id = artist["_id"]

	users = db.Users.find()
	for user in users:
		client.messages.create(to=user["UserNumber"], from_="+16505390580", body=artist_name + artist_genre + artist_description + artist_link)

def is_user(phone_number):
	client = get_connection()
	db = client['textchella']
	result = db.Users.find({"UserNumber": phone_number})

	if result.count() == 0:
		return False
	else:
		return True
    
def subscribe(phone_number):
	client = get_connection()
	user_collection = client['textchella']['Users']
	user_collection.insert({
		"UserNumber": phone_number
	})

if __name__ == '__main__':
	text_chella()
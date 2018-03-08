from pymongo import MongoClient

def get_connection():
	user = "stamizharasu"
	password = "Shyam1624abc"
	mlab_url = "ds261678.mlab.com:61678/textchella"
	return MongoClient("mongodb://"+user+":"+password+"@"+mlab_url)
    

def text_chella():
    return 1

def is_user(phone_number):
	client = get_connection()
	db = client['textchella']
	result = db.Users.find()
	#user_collection = client['textchella']['Users']
	#user = user_collection.find({"UserNumber": phone_number})
	#user = user_collection.find()

	print(result.count())

	# if user.count() == 0:
	# 	return False
	# else:
	# 	return True
    
def subscribe(phone_number):
	client = get_connection()
	user_collection = client['textchella']['Users']
	user_collection.insert({
		"UserNumber": phone_number
	})

if __name__ == '__main__':
	print(is_user("+12038565701"))
	#print(is_user("+54634634536"))
	#subscribe("17264712648164")



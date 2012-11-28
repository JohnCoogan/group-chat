##
# Reply / cc all bot for 1011 Rosa
# Scans the bros feed and automatically 
# tweets everyone if @Rosa1011 is mentioned.
##
from ssl import SSLError

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy.utils import import_simplejson

json = import_simplejson()

ROOMMATES = ['johncoogan', 'Dteln', 'thecauble', 'hunterscott', 'robrhinehart']

def tweetToAll(tweet):
	reply_id = tweet['id']
	status_text = tweet['text'].replace('@1011Rosa ','').replace('@1011Rosa','')
	sender_name = tweet['user']['screen_name']
	if sender_name == 'johncoogan':
		status_text += " -JC"
	elif sender_name == 'Dteln':
		status_text += " -DR"
	elif sender_name == 'thecauble':
		status_text += " -MC"
	elif sender_name == 'hunterscott':
		status_text += " -HS"
	elif sender_name == 'robrhinehart':
		status_text += " -RR"
	else:
		status_text += " -@" + sender_name
	for mate in ROOMMATES:
		if sender_name == mate or sender_name == '1011Rosa':
			pass
		else:
			bro_text = "@" + mate + " " + status_text
			try:
				api.update_status(in_reply_to_status_id=reply_id,status=bro_text)
				print "Tweeted: " + bro_text
			except TweepError:
				print "Error: Couldn't tweet: " + bro_text

class TweetListener(StreamListener):
	""" A listener handles tweets are the received from the stream. 
	This checks if they are from us.
	"""
	def on_data(self, data):
		"""Called when raw data is received from connection.
		Override this method if you wish to manually handle
		the stream data. Return False to stop stream and close connection.
		"""
		if 'entities' in data:
			tweet = json.loads(data)
			if 973543512 in [x['id'] for x in tweet['entities']['user_mentions']]:
				tweetToAll(tweet)

		elif 'delete' in data:
			delete = json.loads(data)['delete']['status']
			if self.on_delete(delete['id'], delete['user_id']) is False:
				return False
		elif 'limit' in data:
			if self.on_limit(json.loads(data)['limit']['track']) is False:
				return False

	def on_error(self, status):
		print status
	def on_limit(self, track):
		print "###### LIMIT ERROR #######"

# Authenticate and create API object.
def openStream():
	listener = TweetListener()
	stream = Stream(auth, listener, timeout=60)  
	connected = False
	while True:
		try: 
			if not connected:
				connected = True
				stream.userstream()
		except SSLError, e:
			print e
			connected = False

if __name__ == "__main__":
	auth = OAuthHandler('g6M5GCsvSIGxy01vTRaTDA', 'O9eAv84csSQJL4tMJJZ216aqmeiW5jlDjrp4nkOIU')
	auth.set_access_token('973543512-avVrf9wego1sZiq27R0auKDmUTsgPwHN4g6TOXkp', 'bZlaMV4ZueN7tafwzntOLCiLEQo8nfm7P7RVXv3AaYw')
	api = API(auth)
	openStream()
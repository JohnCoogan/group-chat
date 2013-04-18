##
# Reply / cc all bot for twitter
# Scans the feed and automatically 
# tweets everyone if the bot is mentioned.
##
from ssl import SSLError

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy.utils import import_simplejson

from json import load as json_loader

json = import_simplejson()

CONFIG = json_loader(open('config.json'))

##
# Core Bot Logic, no need to change anything below.
##
def tweetToAll(tweet):
	reply_id = tweet['id']
	# remove mention of bot & trailing space
	status_text = tweet['text'].replace('@' + CONFIG['BOT_NAME'] + ' ','').replace('@' + CONFIG['BOT_NAME'],'')
	sender_name = tweet['user']['screen_name']
	status_text += '" -' + sender_name
	for friend in CONFIG['FRIENDS']:
		if sender_name == friend or sender_name == CONFIG['BOT_NAME']:
			pass
		else:
			send_text = '@' + friend + ' "' + status_text
			try:
				api.update_status(in_reply_to_status_id=reply_id,status=send_text[:140])
				print 'Tweeted: ' + send_text
			except TweepError:
				try:
					api.update_status(status="@%s Sorry, I couldn't send that Tweet out, something went wrong!" % sender_name)
				except TweepError:
					print 'Error: Failed to tweet: ' + send_text

class TweetListener(StreamListener):
	# A listener handles tweets are the received from the stream. 
	# This checks if they are from the list of friends.
	def on_data(self, data):
		# Called when raw data is received from connection.
		# Return False to stop stream and close connection.
		if 'entities' in data:
			tweet = json.loads(data)
			if CONFIG['BOT_NAME'] in [x['screen_name'] for x in tweet['entities']['user_mentions']]:
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

# Opens a Tweepy Stream and passes tweets when they are received.
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

# Authenticate and create API object.
if __name__ == "__main__":
	auth = OAuthHandler(CONFIG['CONSUMER_KEY'], CONFIG['CONSUMER_SECRET'])
	auth.set_access_token(CONFIG['ACCESS_TOKEN'], CONFIG['ACCESS_SECRET'])
	api = API(auth)
	openStream()
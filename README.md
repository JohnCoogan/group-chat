Group Chat for Twitter
======================

This Python script allows a group of friends to easily share a tweet with each other.
After creating a memorable Twitter handle and authenticating with the Twitter API, the bot will pull the Twitter stream and listen for mentions. When anyone in the group mentioned the bot, the Tweet will be quoted and sent to the rest of the group.

Twitter Rate Limits
-------------------
Keep in mind that the Twitter rate limits apply not only to API calls but tweets themselves. Tweets are currently limited to 1000 per day broken into semi-hourly intervals. This works out to about 20 per half hour. If you try and use this with a large group, you will bump into this limit very frequently. I find it works best for groups of 5.
More info: https://support.twitter.com/articles/15364-about-twitter-limits-update-api-dm-and-following

Files
------
* 	groupchat.py: Main script logic
*	Procfile: Runs the script as a worker on heroku.
*	requirements.txt: Ensures Tweepy is installed.

Setup
------------------
Only a few variables need to be changed to get this up an running.
1 	Create a new account for the bot: http://twitter.com
2 	Register for a developer account and create an app: http://dev.twitter.com
3	Create an OAuth token for your app and copy the keys over to groupchat.py
4	Make sure the bot is following your desired list of friends and add their handles to the list.
5	Test by tweeting at the bot!

Deployment
------------------
This script can easily be deployed to Heroku, AWS, or any server host with reasonable uptime.

For Heroku (the simplist IMO):
	1 	heroku create [optional name]
	2 	git push heroku master
	3	heroku ps:scale worker=1
	4	Test by tweeting at the bot / checking heroku logs

Contact me on Twitter about anything: [@JohnCoogan](http://twitter.com/johncoogan)
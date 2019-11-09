import request
import  json
import random
import tweepy as tw
import urllib
from app.const_ENV import *

def get_twitter_url(hashtag):
	auth = tw.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tw.API(auth, wait_on_rate_limit=True)
	search_words = "#"+str(hashtag)+ " -filter:retweets"
	date_since = "2010-01-01"
	tweets = tw.Cursor(api.search,q=search_words,lang="en",since=date_since).items(50)
	user_name=[]
	tweet_id=[]
	for tweet in tweets:
	    user_name.append(tweet.user.screen_name)
	    tweet_id.append(tweet.id)
	if not user_name:
		return None
	random_number = random.randint(0,len(user_name)-1)
	req = "https://publish.twitter.com/oembed?url=https://twitter.com/"+str(user_name[random_number])+"/status/"+str(tweet_id[random_number])+"&hide_thread=true&hide_media=true"
	response = urllib.request.urlopen(req)
	data = json.loads(response.read())
	return data['html']

def save_text(text, label, lang):
	if lang=="en":
		f = open("Hateful_Tweets.txt", "a")
		f.write(text+label+"\n")
		f.close()
	else:
		f = open("German_Hateful_Tweets.txt", "a")
		f.write(text+label+"\n")
		f.close()
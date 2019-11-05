from flask import render_template, flash, redirect, url_for
import urllib.request
from app import app
from app.forms import ModelLanguageForm, HashtagForm
from app.semodel import analyze_eng_text
from app.germodel import analyze_ger_text
import  json
import urllib.request
import tweepy as tw
import pandas as pd
import random


def get_twitter_url(hashtag):
	consumer_key= 'ifAHFrqn2EB3YccxZaT4Bn2yQ'
	consumer_secret= 'ef9M7hRrJhP8xfuaQ0T1APn2U7Rr36uFvbfy6B8BRywoqMv3bX'
	access_token= '1176761735224659968-txABLjzyrJvHlm89GERBoJVPPO1faj'
	access_token_secret= 'db26odDpMAi4WB3rDdXwcDfJAbjYuot6kNasOcstHF9nX'
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



@app.route('/', methods=['GET', 'POST'])
@app.route('/text', methods=['GET', 'POST'])
def text():
    form = ModelLanguageForm()
    h_form = HashtagForm()
    if form.validate_on_submit():
        if form.text.data:
        	if form.model_language.data == 'en':
	        	message, hate_speech = analyze_eng_text(form.text.data)
	        else:
	        	message, hate_speech = analyze_ger_text(form.text.data)
	        flash('{}'.format(message))
	        form.text_color=hate_speech
        return render_template('text_check.html', form=form, h_form=h_form)
    if h_form.validate_on_submit():
    	if h_form.hashtag.data:
    		tweet_url = get_twitter_url(h_form.hashtag.data)
    		if not tweet_url:
    			h_form.ht = h_form.hashtag.data
    			h_form.iframe = "No Tweets were found."
    			return render_template('text_check.html', form=form, h_form=h_form)
    		h_form.ht = h_form.hashtag.data
    		h_form.iframe = tweet_url
    		return render_template('text_check.html', form=form, h_form=h_form)
    return render_template('text_check.html', form=form, h_form=h_form)



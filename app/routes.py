from flask import render_template, flash, redirect, url_for, session
from app import app
from app.forms import ModelLanguageForm, HashtagForm, FeedbackForm
from app.semodel import analyze_eng_text
from app.germodel import analyze_ger_text
from app.common_functions import get_twitter_url, save_text


@app.route('/', methods=['GET', 'POST'])
@app.route('/text', methods=['GET', 'POST'])
def text():
    form = ModelLanguageForm()
    h_form = HashtagForm()
    fb_form = FeedbackForm()
    if form.validate_on_submit():
        if form.text.data:
        	if form.model_language.data == 'en':
	        	message, hate_speech = analyze_eng_text(form.text.data)
	        else:
	        	message, hate_speech = analyze_ger_text(form.text.data)
	        flash('{}'.format(message))
	        form.text_color=hate_speech
	        session['text']=form.text.data
	        session['hate_speech']=hate_speech
	        session['lang']=form.model_language.data
        return render_template('text_check.html', form=form, h_form=h_form, fb_form=fb_form)
    if fb_form.validate_on_submit():
    	if fb_form.submit_da.data and session['hate_speech']:
    		label = " NOT OFFENSIVE PER USER"
    		save_text(session['text'], label, session['lang'])
    	elif fb_form.submit_da.data and not session['hate_speech']:
    		label = " OFFENSIVE PER USER"
    		save_text(session['text'], label, session['lang'])
    if h_form.validate_on_submit():
    	if h_form.hashtag.data:
    		tweet_url = get_twitter_url(h_form.hashtag.data)
    		if not tweet_url:
    			h_form.ht = h_form.hashtag.data
    			h_form.iframe = "No Tweets were found."
    			return render_template('text_check.html', form=form, h_form=h_form)
    		h_form.ht = h_form.hashtag.data
    		h_form.iframe = tweet_url
    		return render_template('text_check.html', form=form, h_form=h_form, fb_form=fb_form)
    return render_template('text_check.html', form=form, h_form=h_form, fb_form=fb_form)



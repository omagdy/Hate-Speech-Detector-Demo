from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length


class ModelLanguageForm(FlaskForm):
    text = TextAreaField('Type text or copy a tweet from Twitter', validators=[Length(min=0, max=280)])
    model_language = SelectField('Language', choices=[('en', 'English'), ('de', 'Deutsch (German)')])
    submit = SubmitField('Analyze Text')

class HashtagForm(FlaskForm):
    hashtag = StringField(u'Search for a random tweet using a Hashtag', validators=[Length(min=0, max=20)])
    submit = SubmitField('Import a random tweet')
    iframe = 0

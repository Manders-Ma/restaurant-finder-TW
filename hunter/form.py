from flask import Flask
from flask_wtf import FlaskForm
from pandas import StringDtype
from wtforms import StringField, RadioField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired()])
    mode = SelectField('Mode', validators=[DataRequired()], choices=[
                       'walking', 'transit', 'driving'])
    mode_para = SelectField('Mode Parameter', choices={
        'None': ('None', 'None'),
        'transit': ('bus', 'rail'),
    })
    time = IntegerField('Time', validators=[DataRequired()])
    search = SubmitField('Search', validators=None)

class ParkingForm(FlaskForm):
    Rname = StringField('Restaurant Name', validators=[DataRequired()])
    search = SubmitField('Search', validators=None)
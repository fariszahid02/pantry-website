# Authored by: Joe
# This file contains the form to input a barcode
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired

class BarcodeForm(FlaskForm):
    barcode = StringField('Barcode', validators=[DataRequired()])
    food = StringField('Food', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    units = StringField('Units', validators=[DataRequired()])
    submit = SubmitField('Submit')
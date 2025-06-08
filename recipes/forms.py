# Authored by: Faris, Joe, Yat Nam, Keirav
# utility functions for recipe management
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired

class IngredientForm(FlaskForm):
    food = StringField('Food', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    unit = StringField('Unit', validators=[DataRequired()])

class RecipeForm(FlaskForm):
    name = StringField('Recipe Name', validators=[DataRequired()])
    method = TextAreaField('Method', validators=[DataRequired()])
    serves = IntegerField('Serving Size', validators=[DataRequired()])
    calories = IntegerField('Calories')
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)
    submit = SubmitField('Add Recipe')

# Authored by: Yat Nam, Jacob, Keirav
# forms for entering shopping list
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class CreateListForm(FlaskForm):
    listName = StringField(validators=[DataRequired()], render_kw={"placeholder": "Shopping List Name"})
    submit = SubmitField("Next")

class AddItemForm(FlaskForm):
    newItem = StringField(validators=[DataRequired()], render_kw={"placeholder": "Food Item"})
    itemQuantity = IntegerField(validators=[DataRequired()], render_kw={"placeholder": "Quantity"})
    itemUnits = StringField(validators=[DataRequired()], render_kw={"placeholder": "Units (e.g., g, ml)"})
    submit = SubmitField("Add Item")





class NewListForm(FlaskForm):
    listName = StringField(validators=[DataRequired()])
    submit = SubmitField()

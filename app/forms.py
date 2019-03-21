from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import Length

class DataForm(FlaskForm):
    equation_field = StringField('Equation', validators=[Length(min=3)])
    result_field = StringField('Result', validators=[])
    errors_field = TextAreaField('Errors', validators=[])

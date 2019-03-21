from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
#from wtforms.validators import DataRequired

class DataForm(FlaskForm):
    equation_field = StringField('Equation', validators=[])
    result_field = StringField('Result', validators=[])
    errors_field = TextAreaField('Errors', validators=[])

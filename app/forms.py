from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class WorkoutForm(FlaskForm):
    type = StringField('Workout Type', validators=[DataRequired()])
    duration = IntegerField('Duration (minutes)', validators=[DataRequired()])
    calories_burned = IntegerField('Calories Burned', validators=[DataRequired()])
    submit = SubmitField('Add Workout')

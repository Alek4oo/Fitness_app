from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    workouts = db.relationship('Workout', backref='user', lazy=True)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Float, nullable=False)
    calories_burned = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, type, duration, user_id):
        self.type = type
        self.duration = duration
        self.user_id = user_id
        self.calories_burned = self.calculate_calories()  # Auto-calculate calories burned

    def calculate_calories(self):
        """Calculate calories burned based on workout type and duration"""
        calorie_rates = {
            "Running": 10,  # Calories per minute
            "Cycling": 8,
            "Swimming": 12,
            "Walking": 5,
            "Strength Training": 7,
            "Yoga": 3
        }
        return calorie_rates.get(self.type, 6) * self.duration  # Default: 6 cal/min

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'duration': self.duration,
            'calories_burned': self.calories_burned,  # Automatically calculated
            'date': self.date
        }
